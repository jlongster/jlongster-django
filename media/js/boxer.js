
define(["/media/js/underscore-min.js",
        "/media/js/raphael-min.js"],
       function () {

    var paper;

    function init() {
        paper = Raphael("cs", 513, 189);
        var cells = make_cells(monster);

        draw(cells);
        //setInterval(function() { blink(cells); }, 1000);
    }
    
    function draw(cells) {
        _.each(cells, function(cell) {
            if(cell.active) {
                var rt = paper.rect(cell.x, cell.y, cells.width, cells.height);
                rt.attr({ "fill": "rgba(0, 0, 0, 0)",
                          "stroke": "rgba(0, 0, 0, 0)" });
                cell.paper = rt;

                setTimeout(function() {
                    rt.animate({ "fill": "rgba(0, 0, 0, 1)" });
                }, Math.random()*1000);

                // rt.mouseover(function() {
                //     if(cell.active) {
                //         this.animate({ "fill": "#FF0000",
                //                        "scale": ".5"}, 500);
                //         cell.hit = true;
                //     }
                // });
            }
        });
    }

    function blink(cells) {
        _.each(cells, function(cell) {
            if(cell.paper && !cell.hit) {
                if(cell.active) {
                    cell.paper.attr("fill-opacity", "0");
                    cell.active = false;
                }
                else {
                    cell.paper.attr("fill-opacity", "1");
                    cell.active = true;
                }
            }
        });
    }
    
    function make_cells(data) {
        var cells = [];
        var xn = data[0].length;
        var yn = data.length;
        var cellx = 513/xn;
        var celly = 189/yn;
        
        for(var x=0; x<xn; x++) {
            for(var y=0; y<yn; y++) {
                var cell = {};
                cell.x = cellx*x;
                cell.y = celly*y;
                cell.active = data[y][x];
                cells.push(cell);
            }
        }

        cells.width = cellx;
        cells.height = celly;
        return cells;
    }
    

    $(init);

       });