// Load the JSON data
d3.json("combined_in_one_processed.json").then(data => {
    const croreFormatter = value => `${(value / 1e7).toFixed(2)} Cr`;

    const margin = { top: 20, right: 100, bottom: 40, left: 90 },
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // Sum denominations by party
    const denominationSumByParty = {};
    data.forEach(d => {
        const party = d["PartyShortName"];
        denominationSumByParty[party] = (denominationSumByParty[party] || 0) + d.Denominations;
    });

    // Convert to array and sort
    const processedData = Object.keys(denominationSumByParty).map(key => ({
        party: key,
        total: denominationSumByParty[key]
    })).sort((a, b) => b.total - a.total);

    // Set up SVG
    const svg = d3.select("#total-by-party-chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // X scale
    const x = d3.scaleLinear()
        .domain([0, d3.max(processedData, d => d.total)])
        .range([0, width]);

    // Y scale
    const y = d3.scaleBand()
        .domain(processedData.map(d => d.party))
        .range([0, height])
        .padding(0.1);

    // Bars
    svg.selectAll(".bar")
        .data(processedData)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("fill", "steelblue")
        .attr("x", 0)
        .attr("y", d => y(d.party))
        .attr("width", d => x(d.total))
        .attr("height", y.bandwidth());

    // Text labels
    svg.selectAll(".label")
        .data(processedData)
        .enter().append("text")
        .attr("class", "label")
        .attr("y", d => y(d.party) + y.bandwidth() / 2 + 4)
        .attr("x", d => x(d.total) + 3)
        .text(d => croreFormatter(d.total))
        .attr("text-anchor", "start")
        .attr("font-size", "12px");

    // X axis
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat(croreFormatter));


    // Y axis
    svg.append("g")
        .call(d3.axisLeft(y));
});




d3.json("combined_in_one_processed.json").then(data => {

    function indianNumberFormatter(num) {
        if (num >= 1e7) { // For crores
            return `${(num / 1e7).toFixed(2)} Cr`;
        } else if (num >= 1e5) { // For lakhs
            return `${(num / 1e5).toFixed(2)} L`;
        } else if (num >= 1e3) { // For thousands
            return `${(num / 1e3).toFixed(2)}k`;
        } else {
            return num.toString();
        }
    }

    const getFrequency = (array) => {
        const map = {};
        array.forEach(item => {
            var key = item["Denominations"];
            if (map[key]) {
                map[key]++;
            } else {
                map[key] = 1;
            }
        });
        return map;
    };

    dataMap = getFrequency(data);

    // Function to convert dataMap into an array of objects
    data = Object.entries(dataMap).map(([denomination, count]) => ({
        denomination,
        count
    }));

    // Create a table and append it to the 'denominationTable' div
    const table = document.createElement('table');
    table.setAttribute('border', '1');

    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headers = ['Denomination', 'Count'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement('tbody');
    data.forEach(rowData => {
        const row = document.createElement('tr');
        Object.values(rowData).forEach(cellData => {
            const cell = document.createElement('td');
            cell.textContent = cellData;
            row.appendChild(cell);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    // Append the table to the div
    document.getElementById('denominationTable').appendChild(table);
});