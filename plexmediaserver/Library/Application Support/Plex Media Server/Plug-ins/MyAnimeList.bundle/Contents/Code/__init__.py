import re
from datetime import datetime

AGENT_NAME = "MyAnimeList.net"
AGENT_LANGUAGES = [Locale.Language.English]
AGENT_PRIMARY_PROVIDER = True
AGENT_ACCEPTS_FROM = [ 'com.plexapp.agents.localmedia', 'com.plexapp.agents.opensubtitles' ]
AGENT_DETAIL_URL = "http://fribbtastic-api.net/fribbtastic-api/services/anime?id="
AGENT_SEARCH_URL = "http://fribbtastic-api.net/fribbtastic-api/services/anime?s="

def Start():
	Log.Info("[" + AGENT_NAME + "] Starting MyAnimeList.net Agent")
	HTTP.CacheTime = CACHE_1WEEK
	
def ValidatePrefs():
	Log.Info("[" + AGENT_NAME + "] There is nothing to validate")
	
def removeASCII(text):
	return re.sub(r'[^\x00-\x7F]+',' ', text)
	
def doSearch(results, media, lang, mediaType):
	
	Log.Info("[" + AGENT_NAME + "] Seaching for Anime...")
	
	# Initialize Variables
	if mediaType == "tv":
		name = removeASCII(media.show)
	elif mediaType == "movie":
		name = removeASCII(media.name)
	
	anime = None			# root Object
	animeID = None			# ID
	animeTitle = None		# Title
	animeYear = None		# Year
	animeMatchScore = None	# MatchScore
	
	# Build the search Url
	searchUrl = AGENT_SEARCH_URL + String.Quote(name, usePlus=True)
	Log.Info("[" + AGENT_NAME + "] search URL build: " + searchUrl)
	
	# Requesting results from search Url
	Log.Info("[" + AGENT_NAME + "] Requesting results")
	xmlResults = XML.ObjectFromURL(searchUrl)
	
	# Are there errors?
	error = xmlResults.xpath("//error//text()")
	
	if len(error) > 0:
		Log.Warn("[" + AGENT_NAME + "] No Animes found for the name " + name)
	else:
		Log.Info("[" + AGENT_NAME + "] Everything OK I found some results")
	
	# loop through the results and add them to the results
	for i in range(len(xmlResults.xpath("//anime"))):
		
		anime = xmlResults.xpath("//anime[%i]" % (i + 1))[0]
		logmsgsearch = "Result #" + str(i + 1) + ": "
		
		# get the ID
		try:
			animeId = str(anime['ID'])
			logmsgsearch += "ID=" + animeId
		except:
			animeId = None
			logmsgsearch += "ID=" + "NA"
		
		# get the title
		try:
			animeTitle = str(anime['title'])
			logmsgsearch += " Title=" + animeTitle
		except:
			animeTitle = None
			logmsgsearch += " Title=" + "NA"
			
		# get the year
		try:
			animeYear = str(anime['firstAired']).split("-")[0]
			logmsgsearch += " Year=" + animeYear
		except:
			animeYear = None
			logmsgsearch += " Year=" + "NA"
			
		# calculate the matchscore
		try:
			animeMatchScore = int(100 - abs(String.LevenshteinDistance(animeTitle, name)))
			logmsgsearch += " Matchscore=" + str(animeMatchScore)
		except:
			animeMatchScore = None
			logmsgsearch += " Matchscore=" + "NA"
		
		Log.Info("[" + AGENT_NAME + "] " + logmsgsearch)
		results.Append(MetadataSearchResult(id = animeId, name = animeTitle, year = animeYear, score = animeMatchScore, lang = Locale.Language.English))
		
	Log.Info("[" + AGENT_NAME + "] Search completed")
	
	return
	
def parseElements(anime, metadata):

	# get and add ID
	try:
		animeId = anime['ID']
		Log.Info("[" + AGENT_NAME + "] ID: " + str(animeId))
		metadata.id = str(animeId)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] ID is not available - " + str(e))
	
	# get and add title
	try:
		animeTitle = anime['title']
		Log.Info("[" + AGENT_NAME + "] Title: " + str(animeTitle))
		metadata.title = str(animeTitle)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Title is not available - " + str(e))
	
	# get and add synopsis
	try:
		animeSynopsis = anime['synopsis']
		Log.Info("[" + AGENT_NAME + "] Synopsis: " + str(animeSynopsis))
		metadata.summary = str(animeSynopsis)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Synopsis is not available - " + str(e))
	
	# get and add score
	try:
		animeScore = anime['score']
		Log.Info("[" + AGENT_NAME + "] Score: " + str(animeScore))
		metadata.rating = float(animeScore)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Score is not available - " + str(e))
	
	# get and add firstAired
	try:
		animeAired = datetime.strptime(str(anime['firstAired']), "%Y-%m-%d")
		Log.Info("[" + AGENT_NAME + "] First Aired: " + str(animeAired))
		metadata.originally_available_at = animeAired
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] First Aired is not available - " + str(e))
	
	# get and add rating
	try:
		animeRating = anime['rating']
		Log.Info("[" + AGENT_NAME + "] Rating: " + str(animeRating))
		metadata.content_rating = str(animeRating)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Rating is not available - " + str(e))
	
	# get and add covers
	try:
		animeCovers = anime['covers']['cover']
		prefDLCovers = Prefs['cover']
		Log.Info("[" + AGENT_NAME + "] Requesting " + prefDLCovers + " Covers")
		
		maxCovers = 0
		
		if prefDLCovers == "all available":
			maxCovers = len(animeCovers)
		else:
			maxCovers = prefDLCovers
		
		if maxCovers > len(animeCovers):
			maxCovers = len(animeCovers)
		
		for i in range(0,int(maxCovers)):
			Log.Info("[" + AGENT_NAME + "] Requesting Cover from Url " + animeCovers[i])
			metadata.posters[str(animeCovers[i])] = Proxy.Media(HTTP.Request(str(animeCovers[i])).content)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Covers are not available - " + str(e))
	
	# get and add duration
	try:
		animeDuration = anime['duration']
		Log.Info("[" + AGENT_NAME + "] Duration: " + str(animeDuration))
		metadata.duration = int(animeDuration)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Duration is not available - " + str(e))
	
	# get and add genres
	try:
		animeGenres = anime['genres']['genre']
		
		logmsggenre = ""
		
		for genre in animeGenres:
			metadata.genres.add(str(genre))
			logmsggenre += " " + genre
			
		Log.Info("[" + AGENT_NAME + "] Genre: " + logmsggenre)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Genres Are not available - " + str(e))
	
	# get and add producers
	try:
		animeProducers = anime['producers']['producer']
		animeStudio = ""
		
		for producer in animeProducers:
			if animeStudio != "":
				animeStudio += ", "
			animeStudio += producer
		
		Log.Info("[" + AGENT_NAME + "] Producers: " + str(animeStudio))
		
		metadata.studio = str(animeStudio)
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Producers Are not available - " + str(e))
	
	# get and add backgrounds
	try:
		animeBackgrounds = anime['backgrounds']['background']
		prefDLBackground = Prefs['background']
		Log.Info("[" + AGENT_NAME + "] Requesting " + prefDLBackground + " Backgrounds")
		
		maxBackgrounds = 0
		
		if prefDLBackground == "all available":
			maxBackgrounds = len(animeBackgrounds)
		else:
			maxBackgrounds = prefDLBackground
		
		if maxBackgrounds > len(animeBackgrounds):
			maxBackgrounds = len(animeBackgrounds)
		
		for i in range(0,int(maxBackgrounds)):
			Log.Info("[" + AGENT_NAME + "] Requesting Background from Url " + str(animeBackgrounds[i]))
			metadata.art[str(animeBackgrounds[i])] = Proxy.Media(HTTP.Request(str(animeBackgrounds[i])).content)
		
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Backgrounds are not available - " + str(e))
	
	# get and add banners
	try:
		animeBanners = anime['banners']['banner']
		prefDLBanner = Prefs['banner']
		Log.Info("[" + AGENT_NAME + "] Requesting " + prefDLBanner + " Banners")
		
		maxBanners = 0
		
		if prefDLBanner == "all available":
			maxBanners = len(animeBanners)
		else:
			maxBanners = prefDLBanner
		
		if maxBanners > len(animeBanners):
			maxBanners = len(animeBanners)
		
		for i in range(0,int(maxBanners)):
			Log.Info("[" + AGENT_NAME + "] Requesting Banners from Url " + animeBanners[i])
			metadata.banners[str(animeBanners[i])] = Proxy.Media(HTTP.Request(str(animeBanners[i])).content)
		
	except Exception, e:
		Log.Warn("[" + AGENT_NAME + "] Banners are not available - " + str(e))
		
	return
	
def doUpdateTV(metadata, media, lang):

	# initialize variables
	anime = None				# root Object
	
	Log.Info("[" + AGENT_NAME + "] Updating TV Show")
	Log.Info("[" + AGENT_NAME + "] Requesting Data for Anime: " + metadata.id)
	
	# build Url
	Log.Info("[" + AGENT_NAME + "] Building Request URL")
	detailUrl = AGENT_DETAIL_URL + String.Quote(metadata.id, usePlus = True)
	Log.Info("[" + AGENT_NAME + "] URL: " + detailUrl)
	
	# requesting data
	Log.Info("[" + AGENT_NAME + "] Requesting data")
	xmlResult = XML.ObjectFromURL(detailUrl)
	
	# parse data and add to metadata
	for i in range(len(xmlResult.xpath("//anime"))):
		
		anime = xmlResult.xpath("//anime[%i]" % (i + 1)) [0]
		
		parseElements(anime, metadata)
				
		# get and add Episodes
		try:
			
			for episode in media.seasons[1].episodes:
				
				logmsgepisode = "Parsing EP #" + episode + ": "
				apiEpisodeTitle = xmlResult.xpath("//anime/episodes/episode[" + episode + "]/engTitle/text()")
				apiEpisodeAired = xmlResult.xpath("//anime/episodes/episode[" + episode + "]/aired/text()")
				defaultTitle = "Episode: " + str(episode)
				
				plexEpisode = metadata.seasons[1].episodes[int(episode)]
				
				# if the API episode title element is 0 there is no title available and needs to be set to a default value
				if len(apiEpisodeTitle) != 0:
					
					plexEpisode.title = str(apiEpisodeTitle[0])
					logmsgepisode += "Title=" + str(apiEpisodeTitle[0])
				
				else:
					if plexEpisode.title == 0:
						plexEpisode.title = defaultTitle
						logmsgepisode += "Title=" + "NA (" + defaultTitle + ")"
					else:
						logmsgepisode += "Title=" + plexEpisode.title + " (current)"
				
				# if the API episode aired element is 0 there is no date available and needs to be set to a default value
				if len(apiEpisodeAired) != 0:
					plexEpisode.originally_available_at = datetime.strptime(str(apiEpisodeAired[0]), "%Y-%m-%d")
					logmsgepisode += " Aired=" + str(apiEpisodeAired[0])
					
				else:
					if plexEpisode.originally_available_at == 0:
						dnow = datetime.now()
						plexEpisode.originally_available_at = dnow
						logmsgepisode += " Aired=" + "NA (" + str(dnow) + ")"
					else:
						logmsgepisode += " Aired=" + str(plexEpisode.originally_available_at) + " (current)"
				
				Log.Info(logmsgepisode)
		except Exception, e:
			Log.Warn("[" + AGENT_NAME + "] Episodes are not available - " + str(e))
		
	return
	
def doUpdateMovie(metadata, media, lang):

	# initialize variables
	anime = None				# root Object
	
	Log.Info("[" + AGENT_NAME + "] Updating Movie")
	Log.Info("[" + AGENT_NAME + "] Requesting Data for Anime: " + metadata.id)
	
	# build Url
	Log.Info("[" + AGENT_NAME + "] Building Request URL")
	detailUrl = AGENT_DETAIL_URL + String.Quote(metadata.id, usePlus = True)
	Log.Info("[" + AGENT_NAME + "] URL: " + detailUrl)
	
	# requesting data
	Log.Info("[" + AGENT_NAME + "] Requesting data")
	xmlResult = XML.ObjectFromURL(detailUrl)
	
	# parse data and add to metadata
	for i in range(len(xmlResult.xpath("//anime"))):
		Log.Info("[" + AGENT_NAME + "] ----- Anime ----- ")
		
		anime = xmlResult.xpath("//anime[%i]" % (i + 1)) [0]
		
		parseElements(anime, metadata)
	
	return

class MyAnimeListTV(Agent.TV_Shows):
	name = AGENT_NAME
	languages = AGENT_LANGUAGES
	primary_provider = AGENT_PRIMARY_PROVIDER
	accepts_from = AGENT_ACCEPTS_FROM
	
	def search(self, results, media, lang, manual):
		doSearch(results, media, lang, "tv")
		return
	
	def update(self, metadata, media, lang, force):
		doUpdateTV(metadata, media, lang)
		return

class MyAnimeListMovie(Agent.Movies):
	name = AGENT_NAME
	languages = AGENT_LANGUAGES
	primary_provider = AGENT_PRIMARY_PROVIDER
	accepts_from = AGENT_ACCEPTS_FROM
	
	def search(self, results, media, lang, manual):
		doSearch(results, media, lang, "movie")
		return
	
	def update(self, metadata, media, lang, force):
		doUpdateMovie(metadata, media, lang)
		return
