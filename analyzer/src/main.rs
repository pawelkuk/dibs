use plotters::prelude::*;
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

#[derive(Debug, serde::Deserialize, Clone)]
struct Reservation {
    time: f64,
    reservation_duration: f64,
    was_successful: bool,
}

fn main() {
    println!("Hello, world!");
    let csvs = find_all_csv_files();
    if csvs.is_empty() {
        println!("No csv files found")
    }
    let experiments = extract_info_from(csvs);
    println!("{:?}", experiments);

    let mut exp_with_data = Vec::new();
    for experiment in &experiments {
        let e = extract_experiment_data(experiment.clone());
        graph_reservations(e.clone(), 30);
        exp_with_data.push(e);
    }
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
    println!("{:?}", distribution);
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
        println!("{:?}", record);
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
