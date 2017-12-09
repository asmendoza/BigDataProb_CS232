//get the total count of tweets for each main url
var mapMainURL= function(){
	emit(this.mainURL,1);
}

//get the total count of distinct main url from the tweets without the searchKeyword:Philippines
var mapMainURLWOPh = function(){
	if(this.searchKeyword != "Philippines")
		emit(this.mainURL,1);
}

var reduceArraySum = function(key,value){
	return Array.sum(value)
}

//db.fakeNews.mapReduce(mapMainURLWOPh,reduceArraySum,{out:"totalMainURLWOPh"})

//mongoexport --host=127.0.0.1 --db test --collection totalMainURLWOPh --type=csv --fields _id,value --out E:\totalMainURLWOPh.csv