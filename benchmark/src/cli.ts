import { Command, Option } from "@commander-js/extra-typings";
import main from "./benchmark";
// working pattern
const program = new Command()
  .addOption(
    new Option("-m, --mode <string>", "mode in which to run benchmark")
      .default("dibs-two-phase-commit", "2pc")
      .choices(["saga", "2pc"])
      .argParser((value) => {
        if (value === "saga") {
          return "dibs";
        } else if (value === "2pc") {
          return "dibs-two-phase-commit";
        } else {
          throw new Error("Invalid mode");
        }
      })
  )
  .addOption(
    new Option(
      "-d, --delay <number>",
      "delay between iterations of requests in seconds"
    )
      .default(5)
      .argParser((value) => parseInt(value))
  )
  .addOption(
    new Option("-n, --number <number>", "number of requests to send per iter")
      .default(1)
      .argParser((value) => parseInt(value))
  )
  .addOption(
    new Option("-i, --iterations <number>", "number of iterations to run")
      .default(10)
      .argParser((value) => parseInt(value))
  )
  .option("-v, --verbose", "verbose output", false)
  .parse(process.argv);

const options = program.opts();

main(options);
