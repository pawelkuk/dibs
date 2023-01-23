import { Command, Option } from "@commander-js/extra-typings";

// working pattern
const program = new Command()
  .addOption(
    new Option("-m, --mode <string>", "mode in which to run benchmark")
      .default("2pc")
      .choices(["saga", "2pc"])
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
  .option("-v, --verbose", "verbose output", false);
const options = program.opts();
