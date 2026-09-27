function appendValue(value) {

    const display = document.getElementById("display");

    if (display.value === "0") {
        display.value = value;
    } else {
        display.value += value;
    }
}


function clearDisplay() {

    document.getElementById("display").value = "0";
}


function deleteLast() {

    const display = document.getElementById("display");

    display.value = display.value.slice(0, -1);

    if (display.value === "") {
        display.value = "0";
    }
}


async function calculate() {

    const display = document.getElementById("display");

    try {

        const response = await fetch("http://127.0.0.1:5000/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                expression: display.value
            })
        });

        const data = await response.json();

        display.value = data.result;

    } catch (error) {

        display.value = "Error";
        console.error(error);

    }
}


/* Open / Close History */

function toggleHistory() {

    const calculator = document.querySelector(".calculator");

    calculator.classList.toggle("show-history");

    if (calculator.classList.contains("show-history")) {
        showHistory();
    }
}


/* Load History */

async function showHistory() {

    const historyDiv = document.getElementById("history");

    try {

        const response = await fetch("http://127.0.0.1:5000/history");

        const data = await response.json();

        historyDiv.innerHTML = "";

        data.forEach(calculation => {

            const expression = calculation[1];
            const result = calculation[2];
            const dateTime = calculation[3];

            historyDiv.innerHTML += `
                <p>
                    <strong>${expression} = ${result}</strong>
                    <br>
                    <small>${dateTime}</small>
                </p>
            `;
        });

    } catch (error) {

        console.error(error);
        historyDiv.innerHTML = "Unable to load history.";

    }
}


/* Clear History */

async function clearHistory() {

    try {

        const response = await fetch("http://127.0.0.1:5000/clear-history", {
            method: "DELETE"
        });

        const data = await response.json();

        console.log(data.message);

        showHistory();

    } catch (error) {

        console.error(error);

    }
}