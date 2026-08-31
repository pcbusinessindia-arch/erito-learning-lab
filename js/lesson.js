// Load the lesson table from Flask

fetch("http://127.0.0.1:5000/api/customers")
    .then(response => response.json())
    .then(customers => {

        const table = document.getElementById("customerTable");

        table.innerHTML = "";

        customers.forEach(customer => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${customer.id}</td>
                <td>${customer.name}</td>
                <td>${customer.city}</td>
            `;

            table.appendChild(row);

        });

    })
    .catch(error => {

        console.error("Error loading customers:", error);

    });


// Hint button

const hintButton = document.getElementById("hintButton");
const hintText = document.getElementById("hintText");

if (hintButton) {

    hintButton.addEventListener("click", function () {

        if (hintText.style.display === "block") {

            hintText.style.display = "none";
            hintButton.textContent = "💡 Show Hint";

        } else {

            hintText.style.display = "block";
            hintButton.textContent = "💡 Hide Hint";

        }

    });

}


// Run SQL query

const runButton = document.getElementById("runButton");

if (runButton) {

    runButton.addEventListener("click", function () {

        const query = document.getElementById("sqlInput").value;

        const result = document.getElementById("queryResult");

        runButton.textContent = "⏳ Running...";
        runButton.disabled = true;

        result.innerHTML = "Running query...";


        fetch("http://127.0.0.1:5000/api/query", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: query
            })

        })

        .then(response => response.json())

        .then(data => {

            result.innerHTML = "";


            // Database error

            if (data.error) {

                const errorMessage = document.createElement("div");

                errorMessage.className = "result-message";

                errorMessage.textContent =
                    "❌ Query Error: " + data.error;

                result.appendChild(errorMessage);

                return;
            }


            // Get expected query from the HTML

            const expectedQuery =
                document.body.dataset.expectedQuery;


            // Normalize query

            const normalizedQuery = query
                .trim()
                .toLowerCase()
                .replace(/\s+/g, " ")
                .replace(/;$/, "");


            // Feedback

            const feedback = document.createElement("div");

            feedback.className = "result-message";


            if (normalizedQuery === expectedQuery) {

                feedback.textContent =
                    "✅ Correct! Great job.";

            } else {

                feedback.textContent =
                    "❌ Not quite. Review the challenge and try again.";

            }

            result.appendChild(feedback);


            // Result table

            const table = document.createElement("table");

            table.className = "result-table";


            const headerRow = document.createElement("tr");


            data.columns.forEach(column => {

                const header = document.createElement("th");

                header.textContent = column;

                headerRow.appendChild(header);

            });


            table.appendChild(headerRow);


            data.rows.forEach(row => {

                const tableRow = document.createElement("tr");


                row.forEach(value => {

                    const cell = document.createElement("td");

                    cell.textContent = value;

                    tableRow.appendChild(cell);

                });


                table.appendChild(tableRow);

            });


            result.appendChild(table);

        })

        .catch(error => {

            result.innerHTML =
                "❌ Could not connect to the SQL server.";

            console.error("Query error:", error);

        })

        .finally(() => {

            runButton.textContent = "▶ Run Query";
            runButton.disabled = false;

        });

    });

}


// Reset button

const resetButton = document.getElementById("resetButton");

if (resetButton) {

    resetButton.addEventListener("click", function () {

        const defaultQuery =
            document.body.dataset.defaultQuery;

        document.getElementById("sqlInput").value =
            defaultQuery;

        document.getElementById("queryResult").innerHTML =
            "Run your query to see the result.";

    });

}