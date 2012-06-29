<script>
var formatDate = d3.time.format('%Y-%m-%d %H:%M:%S');


var meta = items.meta
var series = []

for (var i=0; i<items.dates.length; i++){
	series[i] = []
	for (var j=0; j<items.dates[i].length; j++){
		series[i][j] = {date: formatDate.parse(items.dates[i][j]), price:items.counts[i][j]}
	}
}

var color = d3.scale.category20c();

var margin = {top: 10, right: 10, bottom: 100, left: 40},
    margin2 = {top: 430, right: 10, bottom: 20, left: 40},
    width = 1600 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom,
    height2 = 500 - margin2.top - margin2.bottom;

var x = d3.time.scale().range([0, width]),
    x2 = d3.time.scale().range([0, width]),
    y = d3.scale.linear().range([height, 0]),
    y2 = d3.scale.linear().range([height2, 0]);

var xAxis = d3.svg.axis().scale(x).orient("bottom"),
    xAxis2 = d3.svg.axis().scale(x2).orient("bottom"),
    yAxis = d3.svg.axis().scale(y).orient("left");

var brush = d3.svg.brush()
    .x(x2)
    .on("brush", brush);

var area = d3.svg.line()
			 .x(function(d) { return x(d.date); })
			 .y(function(d) { return y(d.price); })
			 .interpolate("monotone");
			 
var area2 = d3.svg.line()
    .x(function(d) { return x2(d.date); })
    .y(function(d) { return y2(d.price); })
    .interpolate("monotone");
    
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    
timelineCol = d3.select("#left-col")
timelineCol.append("svg").attr("d", svg);

svg.append("defs").append("clipPath")
    .attr("id", "clip")
    .append("rect")
    .attr("width", width)
    .attr("height", height);

var focus = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    
var context = svg.append("g")
    .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")"); 

//Find extent of x domain and the max value of y domain. Iterate over all extents and find the largest extent
//x domain must be scaled according to the largest extent
var maxx = d3.max(series[0].map(function(d) { return d.date; }));
var minx = d3.min(series[0].map(function(d) { return d.date; }));
var maxy = 0;
for (var i=0; i<series.length; i++){
	var temp_maxx = d3.max(series[i].map(function(d) { return d.date; }));
	if (temp_maxx > maxx){
		maxx = temp_maxx;
	}
	var temp_minx = d3.min(series[i].map(function(d) { return d.date; }));
	if (temp_minx < minx){
		minx = temp_minx;
	}
	var temp_maxy = d3.max(series[i].map(function(d) { return d.price; }));
	if (temp_maxy > maxy){
		maxy = temp_maxy;
	}
}
console.log(maxx);
console.log(minx);

//Sets the x domain to be equal to the width of the extent	
x.domain([minx, maxx]);
y.domain([0, maxy]);
x2.domain(x.domain());
y2.domain(y.domain());

//Appends the large chart
focus.selectAll(".line")
    .data(series)
    .enter()
    .append("path")
    .attr("clip-path", "url(#clip)")
    .attr("d", area)
    .attr("stroke", function(d, i) {return color(i)})
    .attr("stroke-width", 3)
    .on("click", click);

//Appends the x axis
focus.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);
		  
//Appends the small chart
context.selectAll(".line")
    .data(series)
    .enter()
    .append("path")
    .attr("d", area2)
	.attr("stroke", function(d, i) {return color(i)});

//Appends the x axis of the small chart
context.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height2 + ")")
    .call(xAxis2);

//Appends the brush of the small chart
context.append("g")
    .attr("class", "x brush")
    .call(brush)
    .selectAll("rect")
    .attr("y", -6)
    .attr("height", height2);

function brush() {
  x.domain(brush.empty() ? x2.domain() : brush.extent());
  focus.selectAll("path").attr("d", area);
  focus.select(".x.axis").call(xAxis);
}

//-------------------EVENT HANDLERS ---------------//

function click(d, i){
	if (meta){
		//Appends events to show coords
		focus.selectAll("circle") 
          .data(meta) 
          .enter() 
          .append("circle") 
          .attr("cx", function(d) { return x(formatDate.parse(d.date)); }) 
          .attr("cy", function(d) {    var date = formatDate.parse(d.date);
                                       for (var i = 0; i<series[0].length; i++) 
          								if (date - series[0][i].date == 0) {
          									return y(series[0][i].price);
          								}
           					      }) 
          .attr("r", 8) 
          .attr("opacity", 1) 
          .attr("fill", d3.rgb(0, 0, 0))
          .on("click", clickDot)
          .on("mouseover", mouseoverDot)
          .on("mouseout", mouseoutDot)
          .append("svg:title").text(function(d) {return "Date: " + d.date + 
          												"\nTitle: " + d.title + 
          												"\nLocation: " + d.locations +
          												"\nUsers: " + d.authors;});
	}
}

function mouseoverDot(d, i){
	var circle = d3.select(this)
	circle.attr("r", 10);
	circle.attr("fill", d3.rgb(255, 0, 0))
}

function mouseoutDot(d, i){
	var circle = d3.select(this)
	circle.attr("r", 8);
	circle.attr("fill", d3.rgb(0, 0, 0))
}

var popup = new Blurb({
    cssClass: "",
    position: "center-center",          
    displayDuration: -1,
    wrap: true
});

function clickDot(d, i){
	console.log(d.keywords);
	console.log(d.authors);
	console.log(d.namedEntities);
	console.log(d.locations);
	var tmpl = $("#users-actions-edit-template").tmpl({uid: "sadsad", email:"sdasads", act:"asdsada"});
	popup.show(tmpl)
}

$('a.close-pop-up-btn').live("click", function(){popup.close();});

</script>


{% end %}

{% block jquery_templates %}
<script id="users-actions-edit-template" type="text/x-jquery-tmpl">
		<div class="container clearfix" style=" width:600px;">	
			<div class="edits">
			<label for="email">Update Email</label>
			<input style="width: 200px;float:left; position:relative;" type="text" id="email-input" value="${email}" />
		<a uid="${uid}" id="update-email-usr-btn" class="button" style="float:left; position:relative;left:10px;">Change</a> 
		<br><br><br><br>
		<a uid="${uid}" id="activate-usr-btn" class="button"  >${act}</a>

		<br> 	
				<a class="close-pop-up-btn" style="float:right; position:relative;  cursor: pointer;">Close</a>

			</div>	
		</div>
</script>
