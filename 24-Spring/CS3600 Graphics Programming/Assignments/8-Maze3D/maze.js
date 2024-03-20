import {drawLines, drawLineStrip, drawQuad, drawVertices3d} from "./shapes2d.js";
import {Bezier, Point2} from "./bezier.js";
import {myRandom} from "./random.js";

class Cell{
    constructor(){
        this.left = true;
        this.bottom = true;
        this.right = true;
        this.top = true;
        this.visited = false;
    }
    
    draw(gl, shaderProgram, x, y){
        // Draw walls as 2D lines:
        const vertices = [];
        if(this.left){
            vertices.push(x,y, x,y+1);
        }
        if(this.bottom){
            vertices.push(x,y, x+1,y);
        }
        if(this.right){
            vertices.push(x+1,y, x+1,y+1);
        }
        if(this.top){
            vertices.push(x,y+1, x+1,y+1);
        }
        drawLines(gl, shaderProgram, vertices, [0,0,0, 1]);

        // Draw walls as 3D quads:
        const r = Math.sin(x * 3712 + y * 34857 + 1) * .5 + .5;
        const g = Math.sin(x * 9321 + y * 27543 + 2) * .5 + .5;
        const b = Math.sin(x * 1268 + y * 12771 + 7) * .5 + .5;
        if(this.left){
            drawQuad(gl, shaderProgram, x,y,0, x,y+1,0, x,y+1,1, x,y,1, r,g,b);
        }
    }
    drawOptimized(gl, shaderProgram, x, y, vertices){

        // Draw walls as 3D quads:
        const r = Math.sin(x * 3712 + y * 34857 + 1) * .5 + .5;
        const g = Math.sin(x * 9321 + y * 27543 + 2) * .5 + .5;
        const b = Math.sin(x * 1268 + y * 12771 + 7) * .5 + .5;
        if(this.left){
            //drawQuad(gl, shaderProgram, x,y,0, x,y+1,0, x,y+1,1, x,y,1, r,g,b);
            vertices.push(x,y,0,r,g,b, x,y+1,0,r,g,b, x,y+1,1,r,g,b);
            vertices.push(x,y,0,r,g,b, x,y+1,1,r,g,b, x,y,1 ,r,g,b);
        }
    }
}

class Maze{
    constructor(WIDTH, HEIGHT){
        this.WIDTH = WIDTH;
        this.HEIGHT = HEIGHT;
        this.cells = [];
        this.path = [];
        for(let r=0; r<HEIGHT; r++){
            this.cells.push([]);
            for(let c=0; c<WIDTH; c++){
                this.cells[r].push(new Cell());
            }
        }
        this.removeWalls(0,0);

        for(let r=0; r<this.HEIGHT; r++){
            for(let c=0; c<this.WIDTH; c++){
                this.cells[r][c].visited = false;
            }
        }
        this.path.push(.5, .5);
        this.path.push(.5, .5);
        this.findPath(0,0);
        this.path.push(WIDTH-.5, HEIGHT-.5);
        this.path.push(WIDTH-.5, HEIGHT-.5);
    }

    removeWalls(c,r){
        this.cells[r][c].visited = true;
        const LEFT = 0;
        const BOTTOM = 1;
        const RIGHT = 2;
        const TOP = 3;
        while(true){
            // which directions are possible from the current cell?
            const available = []; 
            if(c>0 && this.cells[r][c-1].visited==false){
                available.push(LEFT);
            }
            if(c<this.WIDTH-1 && this.cells[r][c+1].visited == false){
                available.push(RIGHT);
            }
            if(r>0 && this.cells[r-1][c].visited==false){
                available.push(BOTTOM);
            }
            if(r<this.HEIGHT-1 && this.cells[r+1][c].visited == false){
                available.push(TOP);
            }

            // if we can't go forwards, go backwards.
            if (available.length == 0){
                return;
            }

            // randomly choose between the available directions, and go there.
            const random = Math.floor(myRandom()*available.length);
            const direction = available[random];

            if(direction==LEFT){
                this.cells[r][c].left = false; // remove my left wall
                this.cells[r][c-1].right = false; // remove the cell to the left's right wall
                this.removeWalls(c-1,r); // recurse left
            }            
            if(direction==RIGHT){
                this.cells[r][c].right = false;
                this.cells[r][c+1].left = false;
                this.removeWalls(c+1,r);
            }
            if(direction==BOTTOM){
                this.cells[r][c].bottom = false; 
                this.cells[r-1][c].top = false;
                this.removeWalls(c,r-1); 
            }  
            if(direction==TOP){
                this.cells[r][c].top = false; 
                this.cells[r+1][c].bottom = false;
                this.removeWalls(c,r+1); 
            }  
        }
    }

    // findPath should return True if this is the end cell, OR if it leads to the end cell.
    // It should return False if this is a loser cell.
    findPath(c,r){
        this.cells[r][c].visited = true;
        this.path.push(c+.5, r+.5);
        if(c==this.WIDTH-1 && r==this.HEIGHT-1){ // the top right cell is the solution
            return true; // this cell is the solution
        }
        // move left if there is no wall, and it hasn't been visited. Return true if it returns true.
        if (!this.cells[r][c].left && !this.cells[r][c-1].visited){
            if (this.findPath(c-1,r)){
                return true; // this cell leads to the solution
            }
        }
        // Same for right, top, and bottom:
        if (!this.cells[r][c].right && !this.cells[r][c+1].visited){
            if (this.findPath(c+1,r)){
                return true;
            }
        }
        if (!this.cells[r][c].top && !this.cells[r+1][c].visited){
            if (this.findPath(c,r+1)){
                return true;
            }
        }
        if (!this.cells[r][c].bottom && !this.cells[r-1][c].visited){
            if (this.findPath(c,r-1)){
                return true;
            }
        }

        // This is a loser cell, so undo the move from this.path, and return false to the previous cell.
        this.path.pop();
        this.path.pop();
        return false;
    }

    drawPath(gl, shaderProgram){
        drawLineStrip(gl, shaderProgram, this.path, [1,0,1,1]);
    }

    getPathPosition(currentTime){
        // Which bezier curve, and which t-value within it?
        let curve = Math.floor(currentTime);
        let t = currentTime - curve;
        if(curve>this.path.length/2-4){
            curve = this.path.length/2-4;
            t = 1.0;
        }
        const bsplinePoints = [];
        for (let i=0; i<4; i++){
            bsplinePoints.push(new Point2(this.path[curve*2+ i*2+0], this.path[curve*2+i*2+1]));
        }
        const bezierPoints = this.bsplineToBezier(bsplinePoints);

        const b = new Bezier(bezierPoints[0], bezierPoints[1], bezierPoints[2], bezierPoints[3]);
        const p = b.evaluate(t);
        const returnVals = [p.x, p.y, 0];
        return returnVals;
    }

    drawPathCurved(gl, shaderProgram){
        for(let curve=0; curve<this.path.length/2-3; curve++){
            
            const bsplinePoints = [];
            for (let i=0; i<4; i++){
                bsplinePoints.push(new Point2(this.path[curve*2+ i*2+0], this.path[curve*2+i*2+1]));
            }
            const bezierPoints = this.bsplineToBezier(bsplinePoints);

            const b = new Bezier(bezierPoints[0], bezierPoints[1], bezierPoints[2], bezierPoints[3]);
            b.drawCurve(gl, shaderProgram);
        }
    }

    bsplineToBezier(bsplinePoints){
        const temp1 = new Point2(bsplinePoints[0].x/3 + 2*bsplinePoints[1].x/3, bsplinePoints[0].y/3 + 2*bsplinePoints[1].y/3);
        const temp2 = new Point2(2*bsplinePoints[1].x/3 + 1*bsplinePoints[2].x/3, 2*bsplinePoints[1].y/3 + 1*bsplinePoints[2].y/3);
        const temp3 = new Point2(1*bsplinePoints[1].x/3 + 2*bsplinePoints[2].x/3, 1*bsplinePoints[1].y/3 + 2*bsplinePoints[2].y/3);
        const temp4 = new Point2(2*bsplinePoints[2].x/3 + 1*bsplinePoints[3].x/3, 2*bsplinePoints[2].y/3 + 1*bsplinePoints[3].y/3);
        const temp5 = new Point2(temp1.x/2 + temp2.x/2, temp1.y/2 + temp2.y/2);
        const temp6 = new Point2(temp3.x/2 + temp4.x/2, temp3.y/2 + temp4.y/2);

        const bezierPoints = [temp5, temp2, temp3, temp6];
        return bezierPoints;
    }

    draw(gl, shaderProgram){
        for(let r=0; r<this.HEIGHT; r++){
            for(let c=0; c<this.WIDTH; c++){
                this.cells[r][c].draw(gl, shaderProgram, c, r);
            }
        }
    }
    drawOptimized(gl, shaderProgram){
        let vertices = [];
        for(let r=0; r<this.HEIGHT; r++){
            for(let c=0; c<this.WIDTH; c++){
                this.cells[r][c].drawOptimized(gl, shaderProgram, c, r, vertices);
            }
        }
        drawVertices3d(gl, shaderProgram, vertices, gl.TRIANGLES);
    }
    isSafe(x,y,radius){ // returns true if the given circle parameters do not intersect any existing wall or corner
        const c = Math.floor(x);
        const r = Math.floor(y);
        const offsetX = x - c;
        const offsetY = y - r;

        // Check if the right wall is there, and our radius overlaps it:
        if (this.cells[r][c].right && offsetX + radius >1)
            return false;

        // Similarily check other three walls:
        if (this.cells[r][c].left && offsetX - radius < 0)
            return false;
        if (this.cells[r][c].top && offsetY + radius > 1)
            return false;
        if (this.cells[r][c].bottom && offsetY - radius < 0)
            return false;

        // Make sure we are not in any corner:
        if (offsetX + radius > 1 && (offsetY + radius>1 || offsetY-radius<0))
            return false;
        if (offsetX - radius < 0 && (offsetY + radius>1 || offsetY-radius<0))
            return false;
        
        return true; // this is a safe location
    }
}

export {Maze};
