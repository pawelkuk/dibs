"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var axios_1 = require("axios");
var uuid_1 = require("uuid");
var constants_1 = require("./constants");
var utils_1 = require("./utils");
var perf_hooks_1 = require("perf_hooks");
function sleep(ms) {
    return new Promise(function (resolve) {
        setTimeout(resolve, ms);
    });
}
function removeDuplicates(items) {
    return items.filter(function (item, index) { return items.indexOf(item) === index; });
}
function pickSeats(seats, max) {
    if (max === void 0) { max = 2; }
    var picked_seats = [];
    for (var i = 0; i < max; i++) {
        var seat = seats[Math.floor(Math.random() * seats.length)];
        picked_seats.push(seat);
    }
    return removeDuplicates(picked_seats);
}
function extractSeat(seat) {
    var digitsPattern = /[0-9]+/g;
    var letterPattern = /[a-zA-Z]+/g;
    var letterMatch = seat.match(letterPattern);
    var digitsMatch = seat.match(digitsPattern);
    if (letterMatch === null || digitsMatch === null) {
        return [];
    }
    else {
        var row = letterMatch[0];
        var column = Number(digitsMatch[0]);
        return [row, column];
    }
}
function makeReservationData(screening, n) {
    if (n === void 0) { n = 1000; }
    var reservations = Array.from(new Array(n).keys()).map(function () {
        var pickedSeats = pickSeats(screening.free_seats, Math.floor(Math.random() * 5) + 1);
        var reservation = {
            customer_id: uuid_1.v4(),
            screening_id: screening.screening_id,
            reservation_number: uuid_1.v4(),
            amount: (10 * pickedSeats.length).toString(),
            currency: "GBP",
            details: { "agreement signed": true },
            seats_data: pickedSeats.map(function (seat) { return extractSeat(seat); })
        };
        return reservation;
    });
    return reservations;
}
function main(options) {
    return __awaiter(this, void 0, void 0, function () {
        var successList, errorList, i, screeningsResponse, reqs, error_1, successStats, errorStats, totalStats;
        var _this = this;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    successList = [];
                    errorList = [];
                    console.log("starting benchmark");
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < options.iterations)) return [3 /*break*/, 9];
                    console.log("next iter!");
                    _a.label = 2;
                case 2:
                    _a.trys.push([2, 5, , 6]);
                    return [4 /*yield*/, axios_1["default"].get(constants_1.API_URL + "/screenings/")];
                case 3:
                    screeningsResponse = _a.sent();
                    reqs = screeningsResponse.data.map(function (screening) { return __awaiter(_this, void 0, void 0, function () {
                        var screeningDetailResponse, screeningDetail, reservationData, error_2;
                        var _this = this;
                        return __generator(this, function (_a) {
                            switch (_a.label) {
                                case 0:
                                    _a.trys.push([0, 2, , 3]);
                                    return [4 /*yield*/, axios_1["default"].get(constants_1.API_URL + "/screenings/" + screening.screening_id + "/")];
                                case 1:
                                    screeningDetailResponse = _a.sent();
                                    screeningDetail = screeningDetailResponse.data;
                                    console.log(screeningDetail.screening_id, screeningDetail.free_seats.length);
                                    if (screeningDetail.free_seats) {
                                        reservationData = makeReservationData(screeningDetail, options.number);
                                        reservationData.map(function (reservation) { return __awaiter(_this, void 0, void 0, function () {
                                            var start, res, end, error_3, end;
                                            return __generator(this, function (_a) {
                                                switch (_a.label) {
                                                    case 0:
                                                        console.log(reservation.seats_data);
                                                        console.log(options.mode);
                                                        start = perf_hooks_1.performance.now();
                                                        _a.label = 1;
                                                    case 1:
                                                        _a.trys.push([1, 3, , 4]);
                                                        return [4 /*yield*/, axios_1["default"].post(constants_1.API_URL + "/" + options.mode, reservation)];
                                                    case 2:
                                                        res = _a.sent();
                                                        end = perf_hooks_1.performance.now();
                                                        successList.push(end - start);
                                                        return [3 /*break*/, 4];
                                                    case 3:
                                                        error_3 = _a.sent();
                                                        end = perf_hooks_1.performance.now();
                                                        utils_1.handleError(error_3);
                                                        return [3 /*break*/, 4];
                                                    case 4: return [2 /*return*/];
                                                }
                                            });
                                        }); });
                                    }
                                    return [3 /*break*/, 3];
                                case 2:
                                    error_2 = _a.sent();
                                    utils_1.handleError(error_2);
                                    return [3 /*break*/, 3];
                                case 3: return [2 /*return*/];
                            }
                        });
                    }); });
                    return [4 /*yield*/, Promise.all(reqs)];
                case 4:
                    _a.sent();
                    return [3 /*break*/, 6];
                case 5:
                    error_1 = _a.sent();
                    debugger;
                    utils_1.handleError(error_1);
                    return [3 /*break*/, 6];
                case 6: return [4 /*yield*/, sleep(options.delay)];
                case 7:
                    _a.sent();
                    _a.label = 8;
                case 8:
                    i++;
                    return [3 /*break*/, 1];
                case 9:
                    successStats = computeStats(successList);
                    errorStats = computeStats(errorList);
                    totalStats = computeStats(successList.concat(errorList));
                    console.log("###### success stats ######");
                    console.log("avg: ", successStats[0]);
                    console.log("min: ", successStats[1]);
                    console.log("max: ", successStats[2]);
                    console.log("median: ", successStats[3]);
                    console.log("number of successes: ", successList.length);
                    console.log("###### error stats ######");
                    console.log("avg: ", errorStats[0]);
                    console.log("min: ", errorStats[1]);
                    console.log("max: ", errorStats[2]);
                    console.log("median: ", errorStats[3]);
                    console.log("number of errors: ", errorList.length);
                    console.log("###### total stats ######");
                    console.log("avg: ", totalStats[0]);
                    console.log("min: ", totalStats[1]);
                    console.log("max: ", totalStats[2]);
                    console.log("median: ", totalStats[3]);
                    console.log("number of requests: ", successList.length + errorList.length);
                    return [2 /*return*/];
            }
        });
    });
}
function computeStats(times) {
    var total = times.reduce(function (a, b) { return a + b; }, 0);
    var avg = total / times.length;
    var min = Math.min.apply(Math, times);
    var max = Math.max.apply(Math, times);
    var median = times.sort()[Math.floor(times.length / 2)];
    return [avg, min, max, median];
}
exports["default"] = main;