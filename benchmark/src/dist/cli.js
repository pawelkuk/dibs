"use strict";
exports.__esModule = true;
var extra_typings_1 = require("@commander-js/extra-typings");
var benchmark_1 = require("./benchmark");
// working pattern
var program = new extra_typings_1.Command()
    .addOption(new extra_typings_1.Option("-m, --mode <string>", "mode in which to run benchmark")["default"]("dibs-two-phase-commit", "2pc")
    .choices(["saga", "2pc"])
    .argParser(function (value) {
    if (value === "saga") {
        return "dibs";
    }
    else if (value === "2pc") {
        return "dibs-two-phase-commit";
    }
    else {
        throw new Error("Invalid mode");
    }
}))
    .addOption(new extra_typings_1.Option("-d, --delay <number>", "delay between iterations of requests in seconds")["default"](5)
    .argParser(function (value) { return parseInt(value); }))
    .addOption(new extra_typings_1.Option("-n, --number <number>", "number of requests to send per iter")["default"](1)
    .argParser(function (value) { return parseInt(value); }))
    .addOption(new extra_typings_1.Option("-e, --error-margin <number>", "error margin for full screening")["default"](1)
    .argParser(function (value) { return parseInt(value); }))
    .addOption(new extra_typings_1.Option("-N, --numbers-of-screenings <number>", "number of screenings to fully book")["default"](1)
    .argParser(function (value) { return parseInt(value); }))
    .addOption(new extra_typings_1.Option("-i, --iterations <number>", "number of iterations to run. 0 means infinite")["default"](10)
    .argParser(function (value) {
    var val = parseInt(value);
    return val === 0 ? Infinity : val;
}))
    .option("-v, --verbose", "verbose output", false)
    .parse(process.argv);
var options = program.opts();
benchmark_1["default"](options);
