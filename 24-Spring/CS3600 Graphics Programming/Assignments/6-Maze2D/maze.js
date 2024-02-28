import {drawLine} from "./shapes2d.js";

class Cell{
    constructor(){
        this.left = true;
        this.bottom = true;
        this.right = true;
        this.top = true;
        this.visited = false;
    }

    draw(gl, shaderProgram, x,y){
        const vertices = [];
        if (this.left){
            vertices.push(x, y, x, y+1);
        }
        if (this.bottom){
            vertices.push(x, y, x+1, y);
        }
        if(this.top){
            vertices.push(x, y+1, x+1, y+1);
        }        
        if(this.right){
            vertices.push(x+1, y, x+1, y+1);
        }
        drawLine(gl, shaderProgram, vertices);
    }
}

class Maze{
    constructor(width, height){
        this.width = width;
        this.height = height;
        this.cells = []
        for(let r=0; r<this.height; r++){
            this.cells.push([])
            for(let c= 0; c<this.width; c++){
                this.cells[r].push(new Cell());
            }
        }
        this.RemoveWalls(0,0);
    }

    RemoveWalls(r,c){
        this.cells[r][c].visited = true;
        const left = 0;
        const bottom = 1;
        const right = 2;
        const top = 3;

        while (true){
            // Find all the directions we could go:
            const possibilities = [];
            if (c>0 && this.cells[r][c-1].visited == false){
                possibilities.push(left);
            }
            // repeat 3 more times

            // if possibilites is none then return

            // randomly choose which direction

            // Go that direction by knocking out walls, and recursing.
        }


    }
    draw(gl, shaderProgram){
        for(let r=0; r<this.height; r++){
            for(let c= 0; c<this.width; c++){
                this.cells[r][c].draw(gl, shaderProgram, c, r);
            }
        }
    }
}

export { Maze };
