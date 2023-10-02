function setup(){
    let message = document.getElementById("message");
    message.innerHTML = "Click on a cell to change its color. Try to make the whole board one color!";
    
    let board = document.getElementById("board");
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.id = `cell_${i}_${j}`;
            cell.addEventListener("click", () => {
                cell.classList.toggle("highlight");
                const next = document.getElementById(`cell_${i+1}_${j}`);
                if (next) {
                    next.classList.toggle("highlight");
                }
                const prev = document.getElementById(`cell_${i-1}_${j}`);
                if (prev) {
                    prev.classList.toggle("highlight");
                }
                const up = document.getElementById(`cell_${i}_${j+1}`);
                if (up) {
                    up.classList.toggle("highlight");
                }
                const down = document.getElementById(`cell_${i}_${j-1}`);
                if (down) {
                    down.classList.toggle("highlight");
                }

                // Check if the board is all one color
                let allOneColor = true;
                for (let i = 0; i < 3; i++) {
                    for (let j = 0; j < 3; j++) {
                        const cell = document.getElementById(`cell_${i}_${j}`);
                        if (!cell.classList.contains("highlight")) {
                            allOneColor = false;
                        }
                    }
                }
                if (allOneColor) {
                    let message = document.getElementById("message");
                    message.innerHTML = "You Win!";
                    
                    // Change the color of each cell to a random color
                    const colors = ["red", "blue", "green", "yellow", "purple", "orange"];
                    for (let i = 0; i < 3; i++) {
                        for (let j = 0; j < 3; j++) {
                            const cell = document.getElementById(`cell_${i}_${j}`);
                            cell.classList.remove("highlight");
                            cell.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                        }
                    }
                }
            });
            board.appendChild(cell);
        }
    }
    // document.getElementById("cell_0_0").classList.add("highlight");
}

function reset() {
    let board = document.getElementById("board");
    board.innerHTML = "";
    setup();
}