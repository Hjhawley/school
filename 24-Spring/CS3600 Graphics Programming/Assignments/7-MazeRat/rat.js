import {drawLineLoop} from "./shapes2d.js";
class Rat{
    constructor(x,y, degrees){
        this.x = x;
        this.y = y;
        this.degrees = degrees;

        this.SPIN_SPEED = 90; // degrees per second
        this.MOVE_SPEED = 1.0; // cells per second
        this.FATNESS = .3; // for bounding circle
    }

    draw(gl, shaderProgram){
        const modelViewMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uModelViewMatrix");
        const modelViewMatrix = mat4.create();
        mat4.translate(modelViewMatrix, modelViewMatrix, [this.x, this.y, 0] );
        mat4.rotate(modelViewMatrix, modelViewMatrix,(this.degrees*Math.PI/180), [0,0,1]);
        gl.uniformMatrix4fv(modelViewMatrixUniformLocation, false, modelViewMatrix);

        const vertices = [.3,0, -.2,.1, -.2,-.1];
        drawLineLoop(gl, shaderProgram, vertices, [0.5,.5,1., 1.]);
    }
    spinLeft(DT){
        this.degrees += this.SPIN_SPEED*DT;
        if (this.degrees >=360){
            this.degrees -= 360;
        }
        if (this.degrees < 0){
            this.degrees += 360;
        }
    }
    scurryForward(DT){
        const dx = Math.cos(this.degrees*Math.PI/180)*this.MOVE_SPEED*DT;
        const dy = Math.sin(this.degrees*Math.PI/180)*this.MOVE_SPEED*DT;   
        this.x += dx;
        this.y += dy; 
    }
    scurryBackwards(DT){
        this.scurryForward(-DT);
    }
    strafeLeft(DT){
        const dx = Math.cos(this.degrees*Math.PI/180)*this.MOVE_SPEED*DT;
        const dy = Math.sin(this.degrees*Math.PI/180)*this.MOVE_SPEED*DT;   
        this.x += -dy;
        this.y += dx; 
    }
}

export {Rat};