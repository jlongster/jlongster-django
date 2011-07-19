
define(function() {
    var canvas = null;
    var ctx = null;
    var queue = [];
    var main_particle = null;
    var diffuser = null;
    var epsilon = .01;

    function init() {
        if(!canvas_support()) {
            $('.no-canvas-message').show();
            return false;
        }

        $('.title').prepend(
            '<canvas id="cs" width="900" height="200"></canvas>'
        );

        $('.title .title-image').remove();
        $('.canvas-message').show();
        
        canvas = $('#cs')[0];
        ctx = canvas.getContext('2d');
        var content = $('#cs');

        $(window).mousemove(function(e) {
            var offset = content.offset();
            set_anchor(e.pageX - offset.left, e.pageY - offset.top);
        });
        
        // Not accurate for some reason
        $(canvas).mouseover(function() {
             setTimeout(heartbeat, 10);                        
        });
        
        //setTimeout(heartbeat, 10);
        test_diffuser();
        return true;
    }

    function canvas_support(){
        return !!document.createElement('canvas').getContext;
    }

    function test_diffuser() {
        diffuser = new Diffuser();
        queue.push(diffuser);
    }

    function load(data, x_offset, y_offset) {
        if(!init())
            return;
        
        var effect = Math.random();
        
        for(var i=0; i<data.length; i++) {
            var info = data[i];                   
            var p = new Particle();

            var x = info[0] + (x_offset ? x_offset : 165.0);
            var y = info[1] + (y_offset ? y_offset : 50.0);

            // if(effect < .5) {
            //     p.x = x + (-Math.random())*150.0;
            //     p.y = y;
            // }
            // else {
            //     p.x = canvas.width/2.0;
            //     p.y = canvas.height/2.0;
            // }

            p.x = x;
            p.y = y;
            p.orig_x = x;
            p.orig_y = y;
            p.scale = info[2];
            p.size = info[2];
            p.color = "rgb(" + info[3] + "," + info[4] + "," + info[5] + ")";
            
            queue.push(p);
            diffuser.add_particle(p);
        }

        heartbeat();
    }

    // function add_particle(x, y) {
    //     var p = new Particle(x, y, 5.0);
    //     queue.push(p);
    //     diffuser.add_particle(p);
    // }

    function add_anchor(x, y) {
        diffuser.add_anchor([x, y], Math.random()*15.0);
    }

    function set_anchor(x, y) {
        diffuser.set_anchor([x, y], 10.0);
    }

    // core

    function heartbeat() {
        update_time();

        ctx.fillStyle = "#FFFFFF";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // This code allows the update procedure to return
        // false to indicate that the item should be removed
        // from the queue. This app doesn't require this
        // anymore (so don't do it for efficiency).
        //
        // queue = _.foldl(queue, [], function(acc, item) {
        //     if(item.update)
        //         item.update()!==false && acc.push(item);
        //     else
        //         acc.push(item);
        //     return acc;
        // });

        var needs_update = 0;
        
        _.each(queue, function(item) {
            item.update && item.update();
            item.render && item.render();

            if(item.orig_x && item.orig_y) {
                if(Math.abs(item.orig_x - item.x) > epsilon ||
                   Math.abs(item.orig_y - item.y) > epsilon) {
                    needs_update = 1;
                }
            }
        });

        if(queue.length > 0 && needs_update) {
            setTimeout(heartbeat, 25);
        }
    }

    // diffuser

    function Diffuser() {
        this.particles = [];
        this.anchors = [];
    }

    Diffuser.prototype = {
        add_particle: function(p) {
            this.particles.push(p);
        },
        
        add_anchor: function(point, power) {
            this.anchors.push([point, power]);
        },

        set_anchor: function(point, power) {
            this.anchors = [];
            this.add_anchor(point, power);
        },

        update: function() {
            for(var i=0; i<this.particles.length; i++) {
                var p1 = this.particles[i];
                var radius = p1.size/2.0;

                function calculate_force(dist) {
                    return Math.pow(.9, dist)*500.0;
                }
                
                for(var x=0; x<this.anchors.length; x++) {
                    var point = this.anchors[x][0];
                    var power = this.anchors[x][1];
                    
                    var vec = [p1.x-point[X], p1.y-point[Y]];

                    var vecu = vec_unit(vec);
                    var dist = vec_length(vec);
                    var force = calculate_force(dist) * power;

                    p1.velocity[X] += vecu[X]*force;
                    p1.velocity[Y] += vecu[Y]*force;
                }

                var to_orig = [p1.orig_x - p1.x, p1.orig_y - p1.y];
                
                p1.velocity[X] += to_orig[X];
                p1.velocity[Y] += to_orig[Y];
                p1.size = (vec_length(to_orig)/5 + 10) * p1.scale;
                p1.color = "rgb(0," + (255-Math.floor(vec_length(to_orig))) + ",0)";
            }
        }
    }

    // particle

    function Particle(x, y, size, color, velocity, scale) {
        size = size || 10.0;

        this.x = x;
        this.y = y;
        this.orig_x = x;
        this.orig_y = y;
        this.size = size;
        this.scale = scale || 1;
        this.color = color || "#FF0000";
        this.velocity = velocity || [0.0, 0.0];
    }

    Particle.prototype = {
        render: function() {
            //ctx.fillStyle = "rgb(0, " + Math.floor((1-this.y/canvas.height)*255) + ", 0)";
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size/2.0, 0.0, Math.PI*2.0, true);
            ctx.closePath();
            ctx.fill();
        },
        
        update: function() {
            var radius = this.size/2.0;
            
            // if(this.x < radius || this.x+radius > canvas.width) {
            //     if(this.x < radius) this.x = radius;
            //     if(this.x+radius > canvas.width) this.x = canvas.width-radius;
            //     this.velocity[X] = -this.velocity[X];
            // }
            
            // if(this.y < radius || this.y+radius > canvas.height) {
            //     if(this.y < radius) this.y = radius;
            //     if(this.y+radius > canvas.height) this.y = canvas.height-radius;
            //     this.velocity[Y] = -this.velocity[Y];
            // }
            
            this.velocity[X] *= .9;
            this.velocity[Y] *= .9;
            this.step();
        },

        step: function() {
            this.x += this.velocity[X] * time_delta();
            this.y += this.velocity[Y] * time_delta();
        }
    }

    // util

    var X = 0;
    var Y = 1;

    function vec_length(v) {
        return Math.sqrt(v[X]*v[X] + v[Y]*v[Y]);
    }

    function vec_unit(v, l) {
        var l = l || vec_length(v);
        return [v[X]/l, v[Y]/l];
    }

    var _time_snapshot = null;
    var _time_delta = null;

    function update_time() {
        var now = epoch();
        
        if(_time_snapshot) {
            _time_delta = now - _time_snapshot;
            _time_snapshot = now;
        }
        else {
            _time_delta = 0.0;
            _time_snapshot = now;
        }

    }

    function time_delta() {
        return _time_delta;
    }

    function epoch() {
        return (new Date()).getTime()/1000.0;
    }

    function random_in_range(start, end) {
        return start + Math.random()*(end-start)
    }

    return { load: load };
});