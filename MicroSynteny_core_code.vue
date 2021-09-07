barChartInit() {
    let _this = this;
    const svg = d3.select('#mainsvg');
    const width = +svg.attr('width');
    const height = +svg.attr('height');
    const margin = {top: 30, right: 30, bottom: 30, left: 200};
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const xScale = d3.scaleLinear()
    .domain([0, d3.max(this.fragment_length, d => d.value)])
    .range([0, innerWidth]);

    const yScale = d3.scaleBand()
    .domain(this.fragment_length.map(d => d.name))
    .range([0, innerHeight])
    .paddingInner(0.6);

    const g = svg.append('g').attr('id', 'maingroup')
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const yAxis = d3.axisLeft(yScale);

    g.append('g').call(yAxis);

    const bandwidth = innerHeight / (2 - 0.6) * (1 - 0.6);
    const step = innerHeight / (2 - 0.6);

    const areaPath1 = d3.area()
    .y0(bandwidth)
    .y1(step)
    .x0(d => xScale(d.start) + (innerWidth - xScale(this.fragment_length[0].value)) / 2)
    .x1(d => xScale(d.end) + (innerWidth - xScale(this.fragment_length[1].value)) / 2);

    g.append('clipPath')
    .attr('id', 'clip')
    .append('rect')
    .attr('width', innerWidth)
    .attr('height', innerHeight);

    let updateFragment = g.append('g')
    .attr('class', 'chart_fragment')
    .selectAll('path.fragment')
    .data(this.fragment_length)
    .enter()
    .append('rect')
    .attr('clip-path', 'url(#clip)')
    .attr('class', 'fragment')
    .attr('width', d => xScale(d.value))
    .attr('height', yScale.bandwidth())
    .attr('fill', '#99CCFF')
    .attr('opacity', 0.5)
    .attr('y', d => yScale(d.name))
    .attr('x', d => (innerWidth - xScale(d.value)) / 2)

    let updateLinks = g.append('g')
    .attr('class', 'chart_links')
    .selectAll('path.links')
    .data(this.links)
    .enter()
    .append('path')
    .attr('clip-path', 'url(#clip)')
    .attr('d', areaPath1)
    .attr('fill', '#999999')
    .attr('opacity', 0.3)
    .attr('stroke', null)
    .on('mouseover', function(d) {
        d3.select(this)
        .attr('fill', '#eb4d4b')
        .attr('opacity', 0.8)
        .append('title')
        .text(d[0].pos + "→" + d[1].pos)
    })
    .on('mouseout', function() {
        d3.select(this)
        .attr('fill', '#999999')
        .attr('opacity', 0.3)
    })
    .on('click', function(d) {
        var seq0 = d[0].pos;
        var seq1 = d[1].pos;
        _this.toSearchMSA(seq0, seq1);
    });

    let updateCDS0 = g.append('g')
    .attr('class', 'chart_cds_0')
    .selectAll('path.cds_0')
    .data(this.cds[0])
    .enter()
    .append('rect')
    .attr('clip-path', 'url(#clip)')
    .attr('class', 'cds_0')
    .attr('width', d => xScale(Math.abs(d.start_pos - d.end_pos)))
    .attr('height', 0.6 * yScale.bandwidth())
    .attr('fill', function(d) {
        if (d.gene_id == _this.gene1) {
            return 'red'
        } else if (d.strand == '+') {
            return '#9b59b6'
        } else {
            return '#130f4a'
        }
    })
    .attr('y', d => yScale(d.parent) + 0.2 * bandwidth)
    .attr('x', d => xScale(d.start_pos - this.border[d.parent]) + (innerWidth  - xScale(this.fragment_length[0].value)) / 2)

    let updateCDS1 = g.append('g')
    .attr('class', 'chart_cds_1')
    .selectAll('path.cds_1')
    .data(this.cds[1])
    .enter()
    .append('rect')
    .attr('clip-path', 'url(#clip)')
    .attr('class', 'cds_1')
    .attr('width', d => xScale(Math.abs(d.start_pos - d.end_pos)))
    .attr('height', 0.6 * yScale.bandwidth())
    .attr('fill', function(d) {
        if (d.gene_id == _this.gene2) {
            return 'red'
        } else if (d.strand == '+') {
            return '#9b59b6'
        } else {
            return '#130f4a'
        }
    })
    .attr('y', d => yScale(d.parent) + 0.2 * bandwidth)
    .attr('x', d => xScale(d.start_pos - this.border[d.parent]) + (innerWidth  - xScale(this.fragment_length[1].value)) / 2)

    let updateGene0 = g.append('g')
    .attr('class', 'chart_gene_0')
    .selectAll('path.gene_0')
    .data(this.gene[0])
    .enter()
    .append('rect')
    .attr('clip-path', 'url(#clip)')
    .attr('class', 'gene_0')
    .attr('width', d => xScale(Math.abs(d.start_pos - d.end_pos)))
    .attr('height', 0.2 * yScale.bandwidth())
    .attr('fill', function(d) {
        if (d.gene_id == _this.gene1) {
            return 'red'
        } else if (d.strand == '+') {
            return '#9b59b6'
        } else {
            return '#130f4a'
        }
    })
    .attr('y', d => yScale(d.parent) + 0.4 * bandwidth)
    .attr('x', d => xScale(d.start_pos - this.border[d.parent]) + (innerWidth - xScale(this.fragment_length[0].value)) / 2)
    .on('mouseover', function(d) {
        d3.select(this)
        .append('title')
        .text(d.gene_id)
    })
    .on('click', function(d) {
        _this.selection_gene = d.gene_id;
        if (d.gene_id.substr(0, 2) == 'AT') {
            _this.Ath10_boxtarget = 1;
            _this.boxtarget = 0;
        } else {
            _this.boxtarget = 1;
            _this.Ath10_boxtarget = 0;
        }
    });

    let updateGene1 = g.append('g')
    .attr('class', 'chart_gene_1')
    .selectAll('path.gene_1')
    .data(this.gene[1])
    .enter()
    .append('rect')
    .attr('clip-path', 'url(#clip)')
    .attr('class', 'gene_1')
    .attr('width', d => xScale(Math.abs(d.start_pos - d.end_pos)))
    .attr('height', 0.2 * yScale.bandwidth())
    .attr('fill', function(d) {
        if (d.gene_id == _this.gene2) {
            return 'red'
        } else if (d.strand == '+') {
            return '#9b59b6'
        } else {
            return '#130f4a'
        }
    })
    .attr('y', d => yScale(d.parent) + 0.4 * bandwidth)
    .attr('x', d => xScale(d.start_pos - this.border[d.parent]) + (innerWidth - xScale(this.fragment_length[1].value)) / 2)
    .on('mouseover', function(d) {
        d3.select(this)
        .append('title')
        .text(d.gene_id)
    })
    .on('click', function(d) {
        _this.selection_gene = d.gene_id;
        if (d.gene_id.substr(0, 2) == 'AT') {
            _this.Ath10_boxtarget = 1;
            _this.boxtarget = 0;
        } else {
            _this.boxtarget = 1;
            _this.Ath10_boxtarget = 0;
        }
    });
    
    let zoom = d3.zoom()
    .scaleExtent([0.5, 10])
    .translateExtent([
        [0, 0],
        [innerWidth, innerHeight]
    ])
    .extent([
        [0, 0],
        [innerWidth, innerHeight]
    ])
    .on('zoom', zoomed)

    svg.call(zoom)

    function zoomed() {
        let t = d3.event.transform;

        let area = areaPath1
        .x0(d => t.applyX(xScale(d.start)) + t.applyX((innerWidth - xScale(_this.fragment_length[0].value)) / 2))
        .x1(d => t.applyX(xScale(d.end)) + t.applyX((innerWidth - xScale(_this.fragment_length[1].value)) / 2));

        updateLinks.attr('d', area);

        updateFragment
        .attr('width', d => t.applyX(xScale(d.value)) - t.x)
        .attr('x', d => t.applyX(((innerWidth - xScale(d.value)) / 2)) + t.x);

        updateCDS0
        .attr('width', d => t.applyX(xScale(Math.abs(d.start_pos - d.end_pos))) - t.x)
        .attr('x', d => t.applyX(xScale(d.start_pos - _this.border[d.parent])) + t.applyX((innerWidth - xScale(_this.fragment_length[0].value)) / 2));

        updateCDS1
        .attr('width', d => t.applyX(xScale(Math.abs(d.start_pos - d.end_pos))) - t.x)
        .attr('x', d => t.applyX(xScale(d.start_pos - _this.border[d.parent])) + t.applyX((innerWidth - xScale(_this.fragment_length[1].value)) / 2));

        updateGene0
        .attr('width', d => t.applyX(xScale(Math.abs(d.start_pos - d.end_pos))) - t.x)
        .attr('x', d => t.applyX(xScale(d.start_pos - _this.border[d.parent])) + t.applyX((innerWidth - xScale(_this.fragment_length[0].value)) / 2));

        updateGene1
        .attr('width', d => t.applyX(xScale(Math.abs(d.start_pos - d.end_pos))) - t.x)
        .attr('x', d => t.applyX(xScale(d.start_pos - _this.border[d.parent])) + t.applyX((innerWidth - xScale(_this.fragment_length[1].value)) / 2));
    }

    d3.selectAll('.tick text').attr('font-size', '1em');

    svg.call(downloadable({
        width: width,
        height: height,
        filename: 'parallel'
    }))
},