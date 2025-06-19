let boids = [];
const BOID_COUNT = 50
// boids or bird-oid - bird like
function setup() {
  createCanvas(400, 400);
  for (let i = 0; i < BOID_COUNT; i++) {
    boids.push(new Boid(random(width), random(height)));
    // initially assigning random positions
  }
}

function draw() {
  background(20,40,20); // draw a background color
  // iterate thru each bird in boids list
  // and 
  for (let b of boids) {
    b.flock(boids);
    b.update();
    b.edges();
    b.show();
  }
}

class Boid {
  constructor(x, y) {
    this.pos = createVector(x, y); // position vector
    this.vel = p5.Vector.random2D()// no particular reason but felt like tadding this .mult(random(1.5, 105));
    // randomized velocity in any possibily direction
    // force and speed gets capped to make sure they dont shoot away
    this.acc = createVector();
    this.maxForce = 0.15;
    this.maxSpeed = 2.5;

    this.tail = [];
    this.tailMax = 50 // keeping track of last 20 positions, to make the trail
    this.size = 2; // thiccness
  }

  flock(boids) {
    // combining three behaviours of separation
    // aligning, and cohesion
    let sep = this.separate(boids).mult(random(3.5,7.5));
    //console.log(sep.x)
    let ali = this.align(boids)//.mult(1.0);
    let coh = this.cohesion(boids)//.mult(1.0);
    this.acc.add(sep).add(ali).add(coh);
    
    if (mouseIsPressed){
      if (mouseX >= 0 && mouseX <= width && mouseY >= 0 && mouseY <= height) {
        let target = createVector(mouseX, mouseY);
        let mouseForce = p5.Vector.sub(target, this.pos).setMag(this.maxSpeed).sub(this.vel).limit(this.maxForce);
        this.acc.add(mouseForce);
        }
      }
    }

  update() {
    // v += a * dt
    // p += v * dt
    // a gets flushed
    this.vel.add(this.acc).limit(this.maxSpeed);
    this.pos.add(this.vel);
    this.acc.mult(0);
    // removing the last copy of trail, once a new one comes up
    this.tail.push(this.pos.copy());
    if (this.tail.length > this.tailMax) this.tail.shift();
  }

  edges() {
    // boundary checks
    if (this.pos.x > width)  this.pos.x = 0;
    if (this.pos.x < 0)      this.pos.x = width;
    if (this.pos.y > height) this.pos.y = 0;
    if (this.pos.y < 0)      this.pos.y = height;
    // in a previous version, several lines would flash,
    // it was due to this wrapping, where the trails had to render across the screen
  }

  show() {
    noFill();
    strokeWeight(this.size);
    
    for (let i = 0; i < this.tail.length - 1; i++) {
      let p1 = this.tail[i];
      let p2 = this.tail[i + 1];
      if (p5.Vector.dist(p1, p2) > 50) continue; // excatly, this line solved it
      let a = map(i, 0, this.tail.length - 1, 20, 80); // maping length with transparency

      stroke(80, 250, 170, a/1.2);
      line(p1.x, p1.y, p2.x, p2.y);
    }
    noStroke();
    fill(80, 250, 100);
    ellipse(this.pos.x, this.pos.y, this.size*1.2, this.size*1.2);
  }

  separate(boids) {
    let desired = 20, steer = createVector(), cnt = 0;
    for (let o of boids) {
      // check all birds, within the range of 20 px radius
      // if any present
      let d = dist(this.pos.x, this.pos.y, o.pos.x, o.pos.y);
      if (o !== this && d < desired) {
        let diff = p5.Vector.sub(this.pos, o.pos).normalize().div(d);
        // subtracting the pos vecots of the neighbouring bird
        // as if the vector needed for moving away through repulsion is being calculated
        // normalising it to make sure all sides are equally valued/ weighted
        // then dividinig by the distance, as the distance will be inversely proportional to the push strength
        steer.add(diff); cnt++;
      }
    }
    if (cnt) steer.div(cnt); // this counter, makes sure that the forces are averaged, and not anything unbounded
    if (steer.mag() > 0) steer.setMag(this.maxSpeed).sub(this.vel).limit(this.maxForce);
    // capping various vectors
    return steer;
  }

  align(boids) {
    let neigh = 50, sum = createVector(), cnt = 0;
    for (let o of boids) {
      if (o !== this && this.pos.dist(o.pos) < neigh) { sum.add(o.vel); cnt++; }
    }
    // using the average velocities of neighbouring birds
    // then capping it
    if (cnt) {
      sum.div(cnt).setMag(this.maxSpeed);
      return p5.Vector.sub(sum, this.vel).limit(this.maxForce);
    }
    return createVector();
  }

  cohesion(boids) {
    let neigh = 50, center = createVector(), cnt = 0;
    for (let o of boids) {
      if (o !== this && this.pos.dist(o.pos) < neigh) { center.add(o.pos); cnt++; }
    }
    // more like centre of mass?
    // average position
    if (cnt) {
      center.div(cnt);
      let desired = p5.Vector.sub(center, this.pos).setMag(this.maxSpeed);
      return p5.Vector.sub(desired, this.vel).limit(this.maxForce);
    }
    return createVector();
  }
}
