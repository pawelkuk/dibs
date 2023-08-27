use plotters::prelude::*;
use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fs::read_dir;

#[derive(Debug, serde::Deserialize, Clone)]
enum Mode {
    Saga,
    TwoPhaseCommit,
}

#[derive(Debug, serde::Deserialize, Clone)]
struct Experiment {
    name: String,
    mode: Mode,
    csv_file: String,
    movie: String,
    concurrent_requests: u32,
    reservations: Vec<Reservation>,
    path: String,
}

#[derive(Clone)]
struct ExperimentResult {
    concurrent_load: u32,
    avg_exp_time_ms: f64,
    std_dev_exp_time_ms: f64,
    avg_reservation_time_ms: f64,
    std_dev_reservation_time_ms: f64,
    avg_success_rate: f64,
    std_dev_success_rate: f64,
}

#[derive(Debug, serde::Deserialize, Clone)]
struct Reservation {
    time: f64,
    reservation_duration: f64,
    was_successful: bool,
}

fn main() {
    let csvs = find_all_csv_files();
    if csvs.is_empty() {
        println!("No csv files found")
    }
    let experiments = extract_info_from(csvs);
    let mut exp_with_data = Vec::new();
    for experiment in &experiments {
        let e = extract_experiment_data(experiment.clone());
        match graph_reservations(e.clone(), 30) {
            Ok(_) => println!("Graphed {}", e.csv_file),
            Err(e) => println!("Error: {}", e),
        }
        match graph_reservations_in_time(e.clone()) {
            Ok(_) => println!("Graphed {}", e.csv_file),
            Err(e) => println!("Error: {}", e),
        }
        exp_with_data.push(e);
    }
    let load_values = uniq_concurrency_values(&exp_with_data);

    let divided_exps = divide_experiments_into_buckets_by_load(exp_with_data, load_values);

    let stats = calculate_statistics(divided_exps);
    match graph_stats(stats) {
        Ok(_) => println!("Graphed stats"),
        Err(e) => println!("Error: {}", e),
    }
}

fn calculate_statistics(data: HashMap<u32, Vec<Experiment>>) -> Vec<ExperimentResult> {
    let mut res = data
        .into_iter()
        .map(|(concurrent_load, exps)| {
            let sum_of_all_reservations = exps.clone().into_iter().fold(0.0, |acc, e| {
                acc + e
                    .reservations
                    .into_iter()
                    .fold(0.0, |acc, r| acc + r.reservation_duration)
            });
            let n_of_all_reservations = exps
                .clone()
                .into_iter()
                .fold(0.0, |acc, e| acc + e.reservations.len() as f64);
            let n_of_all_experiments = exps.len();
            let avg_reservation_time_ms = sum_of_all_reservations / n_of_all_reservations;
            let sum_of_all_exp_times = exps.clone().into_iter().fold(0.0, |acc, e| {
                acc + e.reservations.into_iter().fold(0.0, |acc, r| {
                    let new_val = r.time + r.reservation_duration;
                    if new_val > acc {
                        new_val
                    } else {
                        acc
                    }
                })
            });
            let avg_exp_time_ms = sum_of_all_exp_times / n_of_all_experiments as f64;
            let sum_of_all_reservations_squared = exps.clone().into_iter().fold(0.0, |acc, e| {
                acc + e
                    .reservations
                    .into_iter()
                    .fold(0.0, |acc, r| acc + r.reservation_duration.powi(2))
            });
            let avg_reservation_time_squared =
                sum_of_all_reservations_squared / n_of_all_reservations;

            let std_dev_reservation_time_ms =
                (avg_reservation_time_squared - avg_reservation_time_ms.powi(2)).sqrt();
            let sum_of_all_exp_times_squared = exps.clone().into_iter().fold(0.0, |acc, e| {
                acc + e.reservations.into_iter().fold(0.0, |acc, r| {
                    let new_val = (r.time + r.reservation_duration).powi(2);
                    if new_val > acc {
                        new_val
                    } else {
                        acc
                    }
                })
            });
            let avg_exp_time_squared = sum_of_all_exp_times_squared / n_of_all_experiments as f64;
            let std_dev_exp_time_ms = (avg_exp_time_squared - avg_exp_time_ms.powi(2)).sqrt();

            let sum_of_all_success_rates = exps.clone().into_iter().fold(0.0, |acc, e| {
                acc + (e
                    .reservations
                    .clone()
                    .into_iter()
                    .fold(0.0, |acc, r| acc + r.was_successful as u32 as f64))
                    / e.reservations.len() as f64
            });
            let avg_success_rate = sum_of_all_success_rates / n_of_all_experiments as f64;
            let sum_of_all_success_rates_squared = exps.into_iter().fold(0.0, |acc, e| {
                acc + ((e
                    .reservations
                    .clone()
                    .into_iter()
                    .fold(0.0, |acc, r| acc + r.was_successful as u32 as f64))
                    / e.reservations.len() as f64)
                    .sqrt()
            });
            let std_dev_success_rate =
                (sum_of_all_success_rates_squared - avg_success_rate.powi(2)).sqrt();

            ExperimentResult {
                concurrent_load,
                avg_reservation_time_ms,
                avg_exp_time_ms,
                std_dev_exp_time_ms,
                std_dev_reservation_time_ms,
                avg_success_rate,
                std_dev_success_rate,
            }
        })
        .collect::<Vec<ExperimentResult>>();
    res.sort_by(|a, b| a.concurrent_load.partial_cmp(&b.concurrent_load).unwrap());
    res
}

fn divide_experiments_into_buckets_by_load(
    exp_with_data: Vec<Experiment>,
    load_values: Vec<u32>,
) -> HashMap<u32, Vec<Experiment>> {
    load_values
        .into_iter()
        .map(|load| {
            let v = exp_with_data
                .clone()
                .into_iter()
                .filter(|exp| exp.concurrent_requests == load)
                .collect();
            (load, v)
        })
        .collect::<HashMap<u32, Vec<Experiment>>>()
}

fn uniq_concurrency_values(exp_with_data: &[Experiment]) -> Vec<u32> {
    exp_with_data
        .iter()
        .map(|exp| exp.concurrent_requests)
        .collect::<HashSet<_>>()
        .into_iter()
        .collect::<Vec<u32>>()
}

struct BoundingBox {
    x_min: f64,
    x_max: f64,
    y_min: f64,
    y_max: f64,
}

fn get_bounding_box(
    data: Vec<ExperimentResult>,
    choose_min_val: impl FnMut(&ExperimentResult) -> f64,
    choose_max_val: impl FnMut(&ExperimentResult) -> f64,
) -> BoundingBox {
    let x_min = data.iter().map(|exp| exp.concurrent_load).min().unwrap() as f64;
    let x_max = data.iter().map(|exp| exp.concurrent_load).max().unwrap() as f64;
    let y_min = data
        .iter()
        .map(choose_min_val)
        .min_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap();
    let y_max = data
        .iter()
        .map(choose_max_val)
        .max_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap();
    BoundingBox {
        x_min,
        x_max,
        y_min,
        y_max,
    }
}

fn graph_stats(stats: Vec<ExperimentResult>) -> Result<(), Box<dyn std::error::Error>> {
    let file_name: String = "graphs/stats.png".to_string();
    let root_area = BitMapBackend::new(file_name.as_str(), (600, 800)).into_drawing_area();
    root_area.fill(&WHITE)?;
    let (upper, lower_tmp) = root_area.split_vertically((64).percent());
    let (_, lower) = lower_tmp.split_vertically((10).percent());
    let avg_exp_bounding_box = get_bounding_box(
        stats.clone(),
        |exp| exp.avg_exp_time_ms - exp.std_dev_exp_time_ms,
        |exp| exp.avg_exp_time_ms + exp.std_dev_exp_time_ms,
    );
    let mut ctx_upper = ChartBuilder::on(&upper)
        .set_label_area_size(LabelAreaPosition::Left, 40)
        .set_label_area_size(LabelAreaPosition::Bottom, 40)
        .caption("Upper", ("sans-serif", 40))
        .build_cartesian_2d(
            avg_exp_bounding_box.x_min..avg_exp_bounding_box.x_max,
            avg_exp_bounding_box.y_min..avg_exp_bounding_box.y_max,
        )?;

    ctx_upper.configure_mesh().draw()?;
    ctx_upper.draw_series(LineSeries::new(
        stats
            .iter()
            .map(|exp| ((exp.concurrent_load as f64), exp.avg_exp_time_ms)),
        &BLUE,
    ))?;

    ctx_upper.draw_series(stats.iter().map(|exp| {
        ErrorBar::new_vertical(
            exp.concurrent_load as f64,
            exp.avg_exp_time_ms - exp.std_dev_exp_time_ms,
            exp.avg_exp_time_ms,
            exp.avg_exp_time_ms + exp.std_dev_exp_time_ms,
            BLUE.filled(),
            20,
        )
    }))?;
    let avg_res_bounding_box = get_bounding_box(
        stats.clone(),
        |exp| exp.avg_reservation_time_ms - exp.std_dev_reservation_time_ms,
        |exp| exp.avg_reservation_time_ms + exp.std_dev_reservation_time_ms,
    );
    let mut ctx_lower = ChartBuilder::on(&lower)
        .set_label_area_size(LabelAreaPosition::Left, 40)
        .set_label_area_size(LabelAreaPosition::Bottom, 40)
        .caption("Lower", ("sans-serif", 40))
        .build_cartesian_2d(
            avg_res_bounding_box.x_min..avg_res_bounding_box.x_max,
            avg_res_bounding_box.y_min..avg_res_bounding_box.y_max,
        )?;

    ctx_lower.configure_mesh().draw()?;

    ctx_lower.draw_series(LineSeries::new(
        stats
            .iter()
            .map(|exp| ((exp.concurrent_load as f64), exp.avg_reservation_time_ms)),
        &BLUE,
    ))?;

    ctx_lower.draw_series(stats.iter().map(|exp| {
        ErrorBar::new_vertical(
            exp.concurrent_load as f64,
            exp.avg_reservation_time_ms - exp.std_dev_reservation_time_ms,
            exp.avg_reservation_time_ms,
            exp.avg_reservation_time_ms + exp.std_dev_reservation_time_ms,
            BLUE.filled(),
            20,
        )
    }))?;

    Ok(())
}

fn graph_reservations_in_time(experiment: Experiment) -> Result<(), Box<dyn std::error::Error>> {
    let file_name: String = format!("graphs/scatter-{}.png", experiment.csv_file);
    let root_area = BitMapBackend::new(file_name.as_str(), (600, 400)).into_drawing_area();
    root_area.fill(&WHITE)?;
    let max = experiment
        .reservations
        .iter()
        .reduce(|a, b| if a.time > b.time { a } else { b })
        .unwrap()
        .time;
    let min = experiment
        .reservations
        .iter()
        .reduce(|a, b| if a.time < b.time { a } else { b })
        .unwrap()
        .time;
    let reservation_duration_max = experiment
        .reservations
        .iter()
        .reduce(|a, b| {
            if a.reservation_duration > b.reservation_duration {
                a
            } else {
                b
            }
        })
        .unwrap()
        .reservation_duration as i32;
    let reservation_duration_min = experiment
        .reservations
        .iter()
        .reduce(|a, b| {
            if a.reservation_duration < b.reservation_duration {
                a
            } else {
                b
            }
        })
        .unwrap()
        .reservation_duration as i32;

    let mut ctx = ChartBuilder::on(&root_area)
        .set_label_area_size(LabelAreaPosition::Left, 40)
        .set_label_area_size(LabelAreaPosition::Bottom, 40)
        .caption("Reservations in time (ms)", ("sans-serif", 40))
        .build_cartesian_2d(
            -(min as i32)..(max as i32),
            -reservation_duration_min..reservation_duration_max,
        )?;

    ctx.configure_mesh().draw()?;

    ctx.draw_series(
        experiment
            .reservations
            .iter()
            .filter(|res| res.was_successful)
            .map(|point| (point.time as i32, point.reservation_duration as i32))
            .map(|point| TriangleMarker::new(point, 5, GREEN)),
    )?;

    ctx.draw_series(
        experiment
            .reservations
            .iter()
            .filter(|res| !res.was_successful)
            .map(|point| (point.time as i32, point.reservation_duration as i32))
            .map(|point| Circle::new(point, 5, RED)),
    )?;
    Ok(())
}

fn get_resolution_and_max(experiment: Experiment, buckets: usize) -> (f64, f64) {
    let max = experiment
        .reservations
        .into_iter()
        .reduce(|a, b| {
            if a.reservation_duration > b.reservation_duration {
                a
            } else {
                b
            }
        })
        .unwrap()
        .reservation_duration;
    ((max / buckets as f64 + 1.0), max)
}

fn extract_distribution(
    experiment: Experiment,
    resolution: f64,
    success: bool,
    buckets: usize,
) -> Vec<u32> {
    let mut distribution = vec![0; buckets];
    for reservation in experiment.reservations {
        if reservation.was_successful != success {
            continue;
        }
        let bucket = (reservation.reservation_duration / resolution) as usize;
        distribution[bucket] += 1;
    }
    distribution
}

fn graph_reservations(
    experiment: Experiment,
    buckets: usize,
) -> Result<(), Box<dyn std::error::Error>> {
    let out_file_name: String = format!("graphs/histogram-{}.png", experiment.csv_file);

    let (resolution, x_max) = get_resolution_and_max(experiment.clone(), buckets);
    let success_distribution = extract_distribution(experiment.clone(), resolution, true, buckets);
    let failed_distribution = extract_distribution(experiment, resolution, false, buckets);
    let y_max = success_distribution
        .iter()
        .chain(failed_distribution.iter())
        .max()
        .unwrap();
    let root = BitMapBackend::new(&out_file_name, (640, 480)).into_drawing_area();

    root.fill(&WHITE)?;

    let mut chart = ChartBuilder::on(&root)
        .x_label_area_size(35)
        .y_label_area_size(40)
        .margin(5)
        .caption("Reservation duration histogram", ("sans-serif", 25.0))
        .build_cartesian_2d((0u32..(x_max as u32)).into_segmented(), 0u32..*y_max)?;

    chart
        .configure_mesh()
        .disable_x_mesh()
        .bold_line_style(WHITE.mix(0.3))
        .y_desc("Count")
        .x_desc("Duration bucket (ms)")
        .axis_desc_style(("sans-serif", 15))
        .draw()?;

    chart.draw_series(
        Histogram::vertical(&chart)
            .style(RED.mix(0.5).filled())
            .data(
                failed_distribution
                    .iter()
                    .enumerate()
                    .map(|(x, y)| ((x * resolution as usize) as u32, *y)),
            ),
    )?;
    chart.draw_series(
        Histogram::vertical(&chart)
            .style(GREEN.mix(0.5).filled())
            .data(
                success_distribution
                    .iter()
                    .enumerate()
                    .map(|(x, y)| ((x * resolution as usize) as u32, *y)),
            ),
    )?;

    // To avoid the IO failure being ignored silently, we manually call the present function
    root.present().expect("Unable to write result to file, please make sure 'plotters-doc-data' dir exists under current dir");
    println!("Result has been saved to {}", out_file_name);

    Ok(())
}

fn find_all_csv_files() -> Vec<std::fs::DirEntry> {
    let paths = read_dir("experiments").unwrap();
    // println!("{}", paths..count());
    let res: Vec<std::fs::DirEntry> = paths
        .into_iter()
        .filter_map(|path| path.ok())
        .filter(|path| path.path().is_file())
        .filter(|path| path.path().extension().unwrap().to_str().unwrap() == "csv")
        .collect();
    res
}

fn extract_experiment_data(mut experiment: Experiment) -> Experiment {
    let path = experiment.path.clone();
    let mut rdr = csv::Reader::from_path(path).unwrap();
    for result in rdr.deserialize() {
        let record: Reservation = result.unwrap();
        experiment.reservations.push(record);
    }
    experiment
}

fn extract_experiment_from_filename(csv: std::fs::DirEntry) -> Result<Experiment, Box<dyn Error>> {
    let filename = csv.file_name().into_string().unwrap();
    let experiment_info: Vec<&str> = filename.split('_').collect();
    let mode = experiment_info[2].to_string();

    let m: Mode;
    if mode == "dibs-two-phase-commit" {
        m = Mode::TwoPhaseCommit;
    } else if mode == "dibs" {
        m = Mode::Saga;
    } else {
        return Err("Mode not supported".into());
    }
    println!("{:?}", experiment_info);
    let experiment = Experiment {
        name: experiment_info[0].to_string(),
        movie: experiment_info[1].to_string(),
        mode: m,
        concurrent_requests: experiment_info[3]
            .strip_suffix(".csv")
            .unwrap()
            .parse::<u32>()
            .unwrap(),
        csv_file: filename.to_string(),
        reservations: Vec::new(),
        path: csv.path().to_str().unwrap().to_string(),
    };
    Ok(experiment)
}

fn extract_info_from(csvs: Vec<std::fs::DirEntry>) -> Vec<Experiment> {
    let mut experiments: Vec<Experiment> = Vec::new();
    for csv in csvs {
        let experiment = extract_experiment_from_filename(csv);
        match experiment {
            Ok(experiment) => {
                experiments.push(experiment);
            }
            Err(e) => println!("Error: {}", e),
        }
    }
    experiments
}
