use std::error::Error;
use std::fs::read_dir;
#[derive(Debug, serde::Deserialize)]
enum Mode {
    Saga,
    TwoPhaseCommit,
}

#[derive(Debug, serde::Deserialize)]
struct Experiment {
    name: String,
    mode: Mode,
    csv_file: String,
    movie: String,
    concurrent_requests: u32,
}

#[derive(Debug, serde::Deserialize)]
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

fn extract_experiment_from_filename(filename: &str) -> Result<Experiment, Box<dyn Error>> {
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
    };
    Ok(experiment)
}

fn read_csv(filename: &str) -> Result<(), Box<dyn Error>> {
    let mut rdr = csv::Reader::from_path(filename).unwrap();
    for result in rdr.deserialize() {
        let record: Reservation = result?;
        println!("{:?}", record);
    }
    Ok(())
}

fn extract_info_from(csvs: Vec<std::fs::DirEntry>) -> Vec<Experiment> {
    let mut experiments: Vec<Experiment> = Vec::new();
    for csv in csvs {
        let filename = csv.file_name().into_string().unwrap();
        let experiment = extract_experiment_from_filename(&filename);
        match experiment {
            Ok(experiment) => {
                experiments.push(experiment);
            }
            Err(e) => println!("Error: {}", e),
        }
    }
    experiments
}
