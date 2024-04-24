import { setShaderAttributes, loadTexture } from "./helpers.js";

class ChessSet {
    constructor(gl) {

    }

    async init(gl) {
        this.blackTexture = loadTexture(gl, 'pieces/PiezasAjedrezDiffuseMarmolBlackBrighter.png', [80, 80, 80, 255]);
        this.whiteTexture = loadTexture(gl, 'pieces/PiezasAjedrezDiffuseMarmol.png', [220, 220, 220, 255]);
        this.boardTexture = loadTexture(gl, 'pieces/TableroDiffuse02.png', [255, 171, 0, 255]);
        this.buffers = {};
        await readObj(gl, "pieces/PiezasAjedrezAdjusted.obj", this.buffers);
    }    

    interpolate(t, t0, t1, v0, v1){
        let ratio = (t - t0) / (t1 - t0);
        ratio = Math.max(ratio, 0);
        ratio = Math.min(ratio, 1);
        return v0 + (v1 - v0) * ratio;
    }

    draw(gl, shaderProgram, currentTime) {
        // Draw the board
        this.drawPiece(gl, shaderProgram, this.boardTexture, "cube", 0.0, 0.0, 0.0);

        // Draw the white pieces, use Math.PI to rotate white pieces 180 degrees
        let [x,y,z] = chessToCoordinates("a1");
        z = this.interpolate(currentTime, 2, 4, z, z-2)
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "rook", x,y,z, Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "knight", ...chessToCoordinates("b1"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "bishop", ...chessToCoordinates("c1"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "queen", ...chessToCoordinates("d1"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "king", ...chessToCoordinates("e1"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "bishop", ...chessToCoordinates("f1"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "knight", ...chessToCoordinates("g1"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "rook", ...chessToCoordinates("h1"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("a2"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("b2"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("c2"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("d2"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("e2"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("f2"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("g2"), Math.PI);
        this.drawPiece(gl, shaderProgram, this.whiteTexture, "pawn", ...chessToCoordinates("h2"), Math.PI);

        // Draw a black pieces
        this.drawPiece(gl, shaderProgram, this.blackTexture, "rook", ...chessToCoordinates("a8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "knight", ...chessToCoordinates("b8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "bishop", ...chessToCoordinates("c8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "queen", ...chessToCoordinates("d8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "king", ...chessToCoordinates("e8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "bishop", ...chessToCoordinates("f8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "knight", ...chessToCoordinates("g8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "rook", ...chessToCoordinates("h8"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("a7"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("b7"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("c7"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("d7"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("e7"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("f7"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("g7"));
        this.drawPiece(gl, shaderProgram, this.blackTexture, "pawn", ...chessToCoordinates("h7"));
    }

    drawPiece(gl, shaderProgram, texture, piece, x, y, z, rotationY = 0) {
        // Bind the texture for the piece
        gl.bindTexture(gl.TEXTURE_2D, texture);
    
        // Make sure to bind the correct buffer before setting attributes
        const pieceBufferInfo = this.buffers[piece];
        if (pieceBufferInfo) {
            gl.bindBuffer(gl.ARRAY_BUFFER, pieceBufferInfo.buffer);
    
            // Set the shader attributes
            setShaderAttributes(gl, shaderProgram);
    
            // Create a model view matrix to move the piece to the desired location
            var modelViewMatrix = mat4.create();
            mat4.translate(modelViewMatrix, modelViewMatrix, [x, y, z]);
    
            // Rotate the piece if a rotation is specified
            if (rotationY !== 0) {
                mat4.rotateY(modelViewMatrix, modelViewMatrix, rotationY);
            }
    
            // Pass the model view matrix to the shader
            gl.uniformMatrix4fv(
                gl.getUniformLocation(shaderProgram, "uModelViewMatrix"),
                false,
                modelViewMatrix
            );
    
            // Draw the piece
            gl.drawArrays(gl.TRIANGLES, 0, pieceBufferInfo.vertexCount);
        } else {
            console.error(`Buffer info for piece ${piece} not found.`);
        }
    }
}

// filename to dictionary this.buffers
async function readObj(gl, filename, buffers) {
    const response = await fetch(filename);
    const text = await response.text()

    const output = {};
    const lines = text.split("\n");
    let objectName = "";
    const vertexList = [];
    const normalList = [];
    const uvList = [];
    let currentFaceList = [];
    output.objectList = {};

    for (const line of lines) {
        const values = line.split(' ');
        if (values[0] == 'o') {
            if (currentFaceList.length > 0) {
                output.objectList[objectName] = currentFaceList
                AddVertexBufferObject(gl, buffers, objectName, vertexList, uvList, normalList, currentFaceList)
                currentFaceList = []
            }
            objectName = values[1];
        }
        else if (values[0] == 'v') {
            vertexList.push(parseFloat(values[1]), parseFloat(values[2]), parseFloat(values[3]))
        }
        else if (values[0] == 'vn') {
            normalList.push(parseFloat(values[1]), parseFloat(values[2]), parseFloat(values[3]))
        }
        else if (values[0] == 'vt') {
            uvList.push(parseFloat(values[1]), 1 - parseFloat(values[2]))
        }
        else if (values[0] == 'f') {
            const numVerts = values.length - 1;
            const fieldsV0 = values[1].split('/');
            for (let i = 2; i < numVerts; i++) {
                const fieldsV1 = values[i].split('/');
                const fieldsV2 = values[i + 1].split('/');
                currentFaceList.push(parseInt(fieldsV0[0]) - 1, parseInt(fieldsV0[1]) - 1, parseInt(fieldsV0[2]) - 1);
                currentFaceList.push(parseInt(fieldsV1[0]) - 1, parseInt(fieldsV1[1]) - 1, parseInt(fieldsV1[2]) - 1);
                currentFaceList.push(parseInt(fieldsV2[0]) - 1, parseInt(fieldsV2[1]) - 1, parseInt(fieldsV2[2]) - 1);
            }
        }
    }
    if (currentFaceList.length > 0) {
        output.objectList[objectName] = currentFaceList
        AddVertexBufferObject(gl, buffers, objectName, vertexList, uvList, normalList, currentFaceList)
    }
    output.vertexList = vertexList;
    output.normalList = normalList;
    output.uvList = uvList;
    return output;
}


function AddVertexBufferObject(gl, buffers, objectName, vertexList, uvList, normalList, currentFaceList) {
    const vertices = [];
    for (let i = 0; i < currentFaceList.length; i += 3) {
        const vertexIndex = currentFaceList[i] * 3;
        const uvIndex = currentFaceList[i + 1] * 2;
        const normalIndex = currentFaceList[i + 2] * 3;
        vertices.push(vertexList[vertexIndex + 0], vertexList[vertexIndex + 1], vertexList[vertexIndex + 2], // x,y,x
            uvList[uvIndex + 0], uvList[uvIndex + 1], // u,v
            normalList[normalIndex + 0], normalList[normalIndex + 1], normalList[normalIndex + 2] // nx,ny,nz
        );
    }

    const vertexBufferObject = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBufferObject);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);

    // Store additional properties as part of the buffer object for easier access later
    buffers[objectName] = {
        buffer: vertexBufferObject,
        vertexCount: vertices.length / 8,
        // Add any additional properties you may need
    };
}

function chessToCoordinates(position) {
    const fileToX = {
        'a': -3.5, 'b': -2.5, 'c': -1.5, 'd': -0.5,
        'e': 0.5, 'f': 1.5, 'g': 2.5, 'h': 3.5
    };
    const rankToZ = {
        '8': -3.5, '7': -2.5, '6': -1.5, '5': -0.5,
        '4': 0.5, '3': 1.5, '2': 2.5, '1': 3.5
    };

    const x = fileToX[position[0]];
    const z = rankToZ[position[1]];
    const y = 0; // As per your system, y is always 0

    return [x, y, z];
}

export { ChessSet };