/*global jQuery:false */
jQuery(document).ready(function ($) {
  "use strict";
  //Camera Jquery
  $("#camera-slide").camera({
    thumbnails: false,
    hover: false,
    fx: "random",
    time: 4000,
    transPeriod: 1000,
    pagination: false,
    loader: "none",
  });
});
