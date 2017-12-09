
////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////

var isFakeNews = function(url){
	var listFakeNews = ["http://www.classifiedtrends.net/","http://definitelyfilipino.com/",
	"http://www.extremereaders.com/","http://www.filipinewsph.com/","http://www.getrealphilippines.com/",
	"https://theguard1an.com/","http://www.kalyepinoy.com/","http://www.leaknewsph.com/",
	"http://www.dutertedefender.com/","http://mindanation.com/","http://www.netizensph.com/",
"http://www.newsmediaph.com/","http://www.newstitans.com/","http://okd2.com/",
"http://www.pinoyfreedomwall.com/","http://pinoytrendingnews.net/","http://www.pinoyviralissues.net/",
"http://pinoyviralnews.com/","http://www.pinoyworld.net/","http://www.tahonews.com/",
"http://www.thevolatilian.com/","ttp://www.socialnewsph.com/","http://www.publictrending.net/",
"http://pinoytrending.altervista.org/","http://www.du30newsinfo.com/","http://www.thinkingpinoy.net/",
"http://www.trendingbalita.info/","http://trendtitan.com/","http://www.trendingnewsportal.net.ph/",]
	
	for(var i = 0; i < listFakeNews.length; i++)
		if(listFakeNews[i] == url)
			return 1;

	return 0;
}

 db.system.js.save( { _id:"isFakeNews",value:isFakeNews})


var mapFakeNewsSiteWithKeyWord = function(){
	if(isFakeNews(this.mainURL) > 0)
		emit({mainUrl:this.mainURL,searchKeyword:this.searchKeyword} ,1);
}


var reduceArraySum = function(key,value){
	return Array.sum(value)
}

db.fakeNews.mapReduce(mapFakeNewsSiteWithKeyWord,reduceArraySum,{out:"fakeNewsSiteWithKeyword"})

mongoexport --host=127.0.0.1 --db test --collection fakeNewsSiteWithKeyword --type=csv --fields _id.mainUrl,_id.searchKeyword,value --out E:\fakeNewsSiteWithKeyword.csv



var mapFakeNewsSite = function(){
		emit(this._id.mainUrl ,{count:this.value});
}

var reduceArraySum = function(key,value){
	var count = 0;
		for(var i = 0; i < value.length; i++)
			count += value[i].count;
	return {count:count};
}

db.fakeNewsSiteWithKeyword.mapReduce(mapFakeNewsSite,reduceArraySum,{out:"fakeNewsSite"})

mongoexport --host=127.0.0.1 --db test --collection fakeNewsSite --type=csv --fields _id,value.count --out E:\fakeNewsSite.csv

////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
 var mapFakeNewsSiteWithKeyWordAndUsers = function(){
	if(isFakeNews(this.mainURL) > 0)
		emit({mainUrl:this.mainURL,searchKeyword:this.searchKeyword,user:this.userScreenName} ,1);
}
