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
    // .domain([1000000, 3000000])
    .range([0, innerWidth]);

    // 用回调函数的形式来将fragment_length中的name属性来赋值给yScale，可以使用这个来绘制我们的染色体
    const yScale = d3.scaleBand()
    .domain(this.fragment_length.map(d => d.name))
    .range([0, innerHeight])
    .paddingInner(0.6);

    // 渲染需要一个容器，而这个就可以提供一个容器，.attr('id', 'maingroup')是给这个容器提供一个id选择器，
    // 这个也相当于是一块SVG的画布，之后的所有操作都在这块画布上进行，可以进行坐标轴渲染，柱状图的柱子的渲染等等。
    const g = svg.append('g').attr('id', 'maingroup')
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

    // const xAxis = d3.axisBottom(xScale);
    // 这个坐标系统是默认将（0,0）放置在左上角的，因此需要将横坐标进行一个移动，把它移动到画布的底端
    // const xGroop = g.append('g').call(xAxis).attr('transform', `translate(${0}, ${innerHeight})`);

    // 利用axisLeft来给坐标轴一个定义，从而来构建坐标轴，但是目前并未对坐标轴进行任何形式的渲染，
    // 仅仅是对坐标轴的一个定义，这个这个axisLeft其实就是一个函数，对yScale来进行一个赋值，这是一种函数式编程
    const yAxis = d3.axisLeft(yScale);
    // call 命令是调用call()中的内容来填上g中的路径
    g.append('g').call(yAxis);

    // 用这个forEach对data的每一个数据进行一个渲染
    // this.fragment_length.forEach(d => {
    //     g.append('rect')
    //     .attr('width', xScale(d.value))
        // 可以使用hetght来控制这个矩形的高度，对我们实现共线性展示也有很大帮助
        // .attr('height', yScale.bandwidth())
        // .attr('fill', '#3498db')
        // .attr('opacity', 0.5)
        // 用yScale（d.name来映射这个矩形应该在的纵坐标位置），如果需要的话可以使用xScale来将其居中显示，这样有利于我们进行共线性的展示
        // .attr('y', yScale(d.name))
        // .attr('x', (innerWidth - xScale(d.value)) / 2)
        // .call(d3.drag()
        // .subject(function() {
        //     const t = d3.select(this);
        //     return {x:t.attr("x"),y:t.attr("y")}
        // })
        // .on('drag', function() {
        //     d3.select(this)
        //     .attr('x', d3.event.x)})
        // );
    // });

    const bandwidth = innerHeight / (2 - 0.6) * (1 - 0.6);
    const step = innerHeight / (2 - 0.6);

    const areaPath1 = d3.area()
    .y0(bandwidth)
    .y1(step)
    .x0(d => xScale(d.start) + (innerWidth - xScale(this.fragment_length[0].value)) / 2)
    // .x0(d => xScale(d.start))
    .x1(d => xScale(d.end) + (innerWidth - xScale(this.fragment_length[1].value)) / 2);

    // this.links.forEach(d => {
    //     g.append('path')
    //     .attr('id', 'links')
    //     .attr('d', areaPath1(d.slice(0, 2)))
    //     .attr('stroke', null)
    //     .attr('fill', '#999999')
    //     .attr('opacity', 0.3)
    //     .on('mouseover', function() {
    //         d3.select(this)
    //         .attr('fill', '#eb4d4b')
    //         .attr('opacity', 0.8)
    //         .append('title')
    //         .text(d[d.length - 1][0] + "→" + d[d.length - 1][1])
    //     })
    //     .on('mouseout', function() {
    //         d3.select(this)
    //         .attr('fill', '#999999')
    //         .attr('opacity', 0.3)
    //     })
    // });

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
        // console.log(seq0, seq1);
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
    // .attr('fill', d => d.strand == '+' ? '#9b59b6' : '#130f4a')
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
    // .attr('fill', d => d.strand == '+' ? '#9b59b6' : '#130f4a')
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
    // .attr('fill', d => d.strand == '+' ? '#9b59b6' : '#130f4a')
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
        // console.log("OKOKOOK")
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
    // .attr('fill', d => d.strand == '+' ? '#9b59b6' : '#130f4a')
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
        // console.log("OKOKOOK")
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
    // g.append('text').text('Genomic Region MicroSynteny')
    // .attr('font-size', '2em')
    // .attr('transform', `translate(${innerWidth/2}, -20)`)
    // text-anchor可以调整text的移动的位置，比如下面的middle，可以设置将其参考位置设置为中间
    // .attr('text-anchor', 'middle');

    svg.call(downloadable({
        width: width,
        height: height,
        filename: 'parallel'
    }))
},