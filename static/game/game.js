function setup(){
    let board = document.getElementById("board");
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.id = `cell_${i}_${j}`;
            cell.addEventListener("click", () => {
                cell.classList.toggle("highlight");
            });
            board.appendChild(cell);
        }
    }
}

function reset() {
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
            cell = document.getElementById(`cell_${i}_${j}`);
            cell.classList.remove("highlight");
        }
    }
}