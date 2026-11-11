/**
 * Symbol: the esτocasτic mark as a superposition. Seven sheets of the mark are stacked and turned apart:
 * a whirl of phases under the one upright mark on top, joined by dashed threads. The pointer observes it:
 * every sheet turns upright and the stack closes into one mark, rippling outwards from the layer touched,
 * which goes bright. Leaving lets the waveform spread again from the same layer. The slider is the
 * stagger, in ms.
 *
 * The pattern: one of many. Two tweens per sheet (its turn and the gap under it), a stagger by distance,
 * static bands for the pick, and a rest that is a composition. Each sheet is a thin plate: its outline,
 * and a second line for its thickness.
 */
const { Cam, clamp, fit, poly, proj, r2, rad, seg, tween, tset, tval, tdone, disposer, mk, pointer, register } = HL;

// The mark's outlines in its own 800 × 590 units: the body, then the two drops.
const BODY = "581,5 585,5 590,5 595,5 600,6 604,7 608,7 611,8 612,9 614,9 616,10 618,11 620,12 621,13 623,13 625,14 626,15 628,17 629,18 631,19 632,20 633,21 634,22 635,24 636,25 637,26 639,28 640,30 640,31 641,33 642,34 642,36 643,37 644,39 644,41 645,43 645,45 645,47 645,49 646,50 646,52 646,54 646,57 646,60 646,64 645,68 645,71 644,75 643,79 643,83 642,87 640,91 639,95 637,100 636,104 635,107 634,109 629,120 618,145 602,179 590,206 585,219 582,225 581,229 580,233 579,235 579,236 579,238 578,240 578,241 579,243 579,244 579,245 580,246 581,248 582,249 583,250 583,250 584,251 585,252 586,252 588,253 589,254 590,254 591,254 592,255 593,255 595,255 598,256 601,256 605,256 611,256 617,256 623,255 630,255 637,254 644,254 652,253 658,252 665,251 671,250 677,249 683,248 689,246 695,244 700,243 704,242 708,240 711,239 715,237 719,235 724,233 728,231 732,229 736,226 740,224 744,221 748,218 752,215 756,212 760,210 764,206 768,203 772,200 776,197 780,193 784,190 788,186 792,182 795,179 796,178 796,178 795,179 796,178 796,177 795,180 790,193 784,209 779,222 777,228 776,229 775,231 774,234 772,237 770,240 769,243 767,246 765,249 763,252 761,254 759,257 757,259 755,262 753,265 751,267 748,270 746,273 744,275 741,278 739,280 736,282 734,285 731,287 729,289 726,291 723,293 720,295 717,297 714,300 711,302 708,303 705,305 702,307 699,308 696,310 693,312 689,313 686,315 683,316 680,318 677,319 673,320 670,321 667,322 663,323 660,324 657,325 654,326 651,327 647,327 644,328 642,329 638,329 640,330 642,330 620,331 551,331 458,332 387,333 357,333 349,333 346,334 341,334 342,334 342,334 340,335 339,335 337,336 336,336 334,337 333,338 332,339 330,340 328,341 326,343 324,345 322,347 319,350 317,353 314,356 312,359 310,362 308,366 305,370 303,374 300,378 298,382 296,387 294,391 291,396 289,402 286,407 284,414 281,422 278,428 277,433 275,438 274,442 273,445 272,448 272,451 271,454 271,458 270,461 270,464 270,467 270,469 270,472 270,474 270,476 271,477 271,479 272,480 273,482 274,484 275,486 276,487 278,489 280,491 281,492 283,494 285,495 287,496 289,497 291,498 293,499 295,500 297,500 299,500 301,501 304,501 306,501 309,501 311,500 313,500 316,500 318,499 321,498 323,497 326,496 329,494 331,493 334,492 336,490 339,488 341,486 345,484 348,481 352,478 355,475 358,473 361,470 364,467 368,463 371,460 374,457 377,453 380,450 382,446 385,443 388,439 390,436 393,432 396,429 399,424 402,419 405,414 408,408 412,402 415,398 415,396 415,397 415,397 415,396 415,395 415,398 414,406 412,417 410,429 408,440 406,450 403,460 400,470 398,480 395,489 392,497 389,504 387,510 384,516 381,521 379,526 377,528 376,530 375,532 374,534 372,536 370,538 369,540 367,542 364,544 363,546 360,549 358,551 353,555 349,559 344,562 340,565 336,567 332,569 329,571 325,573 321,575 317,576 312,578 308,579 304,580 300,581 296,582 292,582 288,583 284,583 281,584 277,584 270,584 256,584 240,584 226,584 220,585 216,585 213,585 210,585 207,585 204,584 201,584 199,584 196,583 193,582 191,582 188,581 186,580 183,579 181,578 179,577 177,576 175,575 173,574 171,572 170,571 168,569 166,568 165,566 163,564 162,562 161,560 160,559 159,557 158,555 157,553 157,551 156,550 156,548 155,546 155,544 155,543 154,541 154,538 154,534 154,530 154,526 155,522 155,520 155,517 156,515 156,512 157,509 158,504 160,499 161,494 162,491 163,488 168,476 180,448 197,412 210,384 214,374 215,371 216,370 217,366 219,362 220,359 220,356 221,353 222,351 222,349 222,348 222,348 221,347 221,346 221,345 221,344 220,343 220,342 219,341 218,341 217,340 217,339 216,338 215,338 214,337 213,337 212,336 210,336 208,335 206,334 204,334 202,334 199,334 192,334 184,334 176,334 168,335 161,335 155,336 148,337 143,337 137,338 132,339 127,340 122,341 117,342 112,343 108,344 103,346 99,347 95,348 92,350 88,351 84,353 80,355 76,357 73,359 69,361 65,363 62,365 58,367 54,370 50,373 46,375 42,378 38,381 34,384 31,387 27,390 23,393 19,397 16,400 12,404 8,408 6,410 4,411 5,411 5,411 8,403 14,386 19,372 22,365 23,361 25,358 27,355 28,352 30,349 32,346 34,343 36,340 38,337 40,334 42,331 44,328 46,325 49,322 51,320 54,317 57,314 60,311 63,308 66,305 70,302 73,300 76,297 79,295 82,293 85,290 89,288 92,286 96,284 100,282 103,280 106,278 110,276 113,275 117,273 121,272 125,270 128,269 132,267 137,266 141,265 145,264 149,263 152,262 156,261 160,261 164,260 160,260 156,260 177,259 247,258 342,258 415,257 444,256 451,256 454,256 458,256 458,256 458,255 459,255 461,255 462,254 463,254 464,253 465,253 467,252 468,251 470,250 471,249 473,247 475,246 476,244 478,242 480,240 482,238 484,236 485,234 487,232 489,230 490,227 492,225 494,222 495,219 497,217 499,214 501,210 504,203 507,196 511,188 515,178 519,168 522,160 524,156 524,153 525,151 526,147 527,144 528,140 528,138 529,135 530,132 530,129 530,126 530,123 530,121 530,119 530,116 530,114 529,113 529,111 529,110 528,109 528,108 527,106 526,105 525,104 523,102 521,99 519,97 517,96 516,95 515,94 514,94 513,93 511,92 509,91 506,90 503,90 501,89 498,89 495,89 492,89 490,89 487,90 484,90 481,91 478,92 475,93 472,95 469,96 466,98 463,100 459,103 455,106 451,109 446,113 443,116 439,119 436,123 432,127 428,131 424,135 421,139 418,143 414,147 411,151 408,156 405,160 402,164 399,169 396,173 392,181 387,189 385,192 385,192 385,192 385,191 385,190 385,188 386,185 387,179 388,172 389,164 390,158 392,153 393,147 394,141 396,135 397,129 398,123 400,118 401,113 403,109 404,104 406,100 407,95 409,91 410,87 412,83 413,80 414,77 416,73 418,70 420,66 422,63 424,60 425,57 427,55 429,53 430,50 433,48 435,46 438,43 440,40 444,37 447,35 450,32 453,30 456,27 460,25 463,23 466,21 469,19 473,18 476,16 479,15 482,14 485,12 488,11 491,11 494,10 497,9 501,8 504,8 507,7 510,7 515,6 520,6 526,5 534,5 547,5 562,5 574,5 578,5 579,5";
const DROP = ["252,102 255,102 260,102 263,102 267,103 271,105 274,106 276,109 278,111 279,112 280,113 281,115 281,116 282,119 282,122 281,125 280,128 279,132 277,135 275,138 272,141 268,144 265,147 261,149 257,151 253,153 248,154 244,155 239,156 235,156 232,156 228,155 224,154 221,153 218,151 216,150 214,148 213,147 212,145 211,143 210,142 210,140 210,138 210,136 210,134 210,132 210,130 211,128 212,126 213,124 214,122 216,120 218,118 219,117 221,115 223,113 225,112 227,110 230,108 233,107 235,106 238,105 240,104 244,103 247,102 249,102", "562,434 566,433 570,434 574,434 577,435 579,435 581,436 582,437 584,438 586,440 589,442 590,444 591,445 591,446 592,448 592,450 592,453 592,456 591,460 590,463 588,467 586,470 583,473 580,476 576,478 572,480 568,482 564,484 560,486 556,487 551,487 547,488 543,488 539,487 535,486 532,485 529,483 527,482 526,480 524,479 523,477 522,476 522,474 521,472 520,470 520,468 520,467 521,464 521,462 522,460 523,458 524,456 525,454 527,452 528,450 530,449 532,447 534,445 536,443 538,442 541,440 543,439 546,438 548,437 551,436 556,435"];

const N = 7, TOP = N - 1, GAP = 5, TIGHT = 1.2, T = 2.4, SC = 0.235, S = 1.8;
const REST = [-112, -88, -66, -47, -30, -14, 0]; // each sheet's turn at rest, bottom to top, in degrees
const K = Math.SQRT1_2;
const pts = (s) => s.split(" ").map((q) => q.split(",").map(Number));
/** A point of the mark on the ground, turned th degrees about its middle, and a quarter of the camera's azimuth so the mark reads upright from it. */
function world([x, y], th) {
  const a = (x - 400) * SC, b = (y - 295) * SC, c = Math.cos(rad(th)), s = Math.sin(rad(th));
  const u = a * c - b * s, v = a * s + b * c;
  return [(u + v) * K, (v - u) * K];
}

function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let step = value, act = -1;
  const body = pts(BODY), outs = [body, ...DROP.map(pts)];

  // The camera is fitted to every turn a sheet can take, so nothing leaves the frame in any pose.
  const C = Cam(45, 0.5, S), box = [];
  for (let i = 0; i < N; i++) for (let f = 0; f <= 4; f++) for (const q of [[0, 0], [800, 0], [0, 590], [800, 590]])
    for (const z of [i * GAP, i * GAP + T]) box.push([...world(q, (REST[i] * f) / 4), z]);
  fit(C, box, 200, 160);
  const P = proj(C), ZS = P(0, 0, 1)[1] - P(0, 0, 0)[1];
  const path = (th) => outs.map((o) => poly(o.map((q) => P(...world(q, th), 0)))).join("");
  const at = (q, th, z) => { const [x, y] = P(...world(q, th), 0); return [x, y + ZS * z]; };

  // Where the dashed threads run: the body's left, right, top and bottom extremes, which turn with their sheet.
  const most = (f) => body.reduce((m, q) => (f(q) > f(m) ? q : m));
  const ends = [most((q) => -q[0]), most((q) => q[0]), most((q) => -q[1]), most((q) => q[1])];

  // Bottom to top. The threads are painted before the sheet above them, so the sheet hides what it should.
  const sheets = [], guides = [];
  for (let i = 0; i < N; i++) {
    if (i) guides.push(ends.map(() => mk("path", { class: "nf dash" }, svg)));
    const g = mk("g", {}, svg);
    const lo = mk("path", { class: "lo" }, g), sil = mk("path", { class: "sil", transform: `translate(0 ${r2(ZS * T)})` }, g);
    sheets.push({ g, lo, sil, tw: tween(REST[i]), gp: tween(GAP), th: REST[i], gap: GAP, z: NaN, drawn: NaN });
  }

  // A sheet's height is the sum of the gaps under it, so the stack can close from any end without two sheets crossing.
  function draw() {
    let z = 0;
    sheets.forEach((s, i) => {
      if (i) z += s.gap;
      if (z !== s.z) { s.z = z; s.g.setAttribute("transform", `translate(0 ${r2(ZS * z)})`); }
      if (s.th === s.drawn) return;
      s.drawn = s.th;
      const d = path(s.th);
      s.lo.setAttribute("d", d); s.sil.setAttribute("d", d);
    });
    guides.forEach((row, i) => row.forEach((el, k) => el.setAttribute("d", seg(at(ends[k], sheets[i].th, sheets[i].z + T), at(ends[k], sheets[i + 1].th, sheets[i + 1].z)))));
  }
  draw();
  const B = register(stage, (_dt, now) => {
    let m = false;
    for (const s of sheets) {
      s.th = tval(s.tw, now); s.gap = tval(s.gp, now);
      if (!tdone(s.tw, now) || !tdone(s.gp, now)) m = true;
    }
    draw();
    return m;
  });
  bag.add(B.unregister);

  const lit = (a) => sheets.forEach((s, i) => s.sil.classList.toggle("hi", i === a));
  lit(TOP);

  // The pick: static bands down the upright mark, which never move, so a sheet turning away cannot change the choice.
  const ys = body.map((q) => P(...world(q, 0), 0)[1]);
  const y0 = Math.min(...ys) + ZS * (TOP * GAP + T), y1 = Math.max(...ys);
  const band = (y) => clamp(TOP - Math.floor(((y - y0) / (y1 - y0)) * N), 0, TOP);

  /** Closes every sheet into the one upright mark (-1 lets the waveform spread); the ripple starts at the layer touched, or the one let go. */
  function apply(from) {
    const now = performance.now();
    sheets.forEach((s, i) => {
      const delay = Math.abs(i - from) * step;
      tset(s.tw, act < 0 ? REST[i] : 0, now, delay);
      tset(s.gp, act < 0 ? GAP : TIGHT, now, delay);
    });
    B.wake();
  }
  function setActive(a) {
    if (a === act) return;
    const from = a >= 0 ? a : act;
    act = a;
    lit(a < 0 ? TOP : a);
    read.textContent = a < 0 ? "rest" : `layer ${a + 1}`;
    apply(from);
  }

  bag.add(pointer(stage, { move: (p) => setActive(band(p[1])), leave: () => setActive(-1) }));
  bag.add(() => svg.replaceChildren());

  return {
    set: (v) => { step = v; },
    destroy: bag.dispose,
  };
}

hairline({
  name: "symbol",
  means: "Seven phases of the mark turned apart: the pointer observes them and they collapse into one mark, rippling out from the layer touched.",
  rules: [1, 2, 5, 8],
  range: [0, 45, 100],
  tour: [[130, 185], [270, 100], null],
  mount,
});
