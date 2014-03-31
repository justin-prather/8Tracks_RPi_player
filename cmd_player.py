from Gr8_Tracks import Gr8_Tracks
import threading
import vlc

is_playing = False
toggle_pause = False
next = False

def play():
	player.get_first_song()
	player.play_song()

	global is_playing
	global toggle_pause
	global next

	is_playing = True
	
	manager = player.vlc_player.event_manager()
	manager.event_attach(vlc.EventType.MediaPlayerEndReached, player.callback)

	player.get_next_song()

	while True:

		while True:
			if is_playing is False:
				player.vlc_player.stop()
				break
			if toggle_pause is True:
				player.vlc_player.pause()
				toggle_pause = False
			if player.at_end or next:
				next = False
				if player.current_song[u'set'][u'at_end'] is True:
					break
				player.at_end = False
				player.current_song = player.next_song
				player.play_song()
				player.get_next_song()

		if is_playing is False:
				break
		player.currentMix_json = player.get_similar_mix()

#======================================================================================

player = Gr8_Tracks( 'ef1b85bdb35b68b0f7ce0f7d6a575c528e600405', 'justin.prather1',
			     'camerasrule')

player.get_play_token()

while True:
	search_type = str(raw_input("Enter search type (all, tags, keyword): "))
	print search_type
	tags = None
	if search_type == "tags":
		tags = str(raw_input("Enter tags separated by spaces: ")).split()

	elif search_type == "keywords":
		tags = str(raw_input("Enter keywords separated by spaces: ")).split()

	search_filter = str(raw_input("Enter filter (recent, all, popular): "))

	search_results = player.search_mix(search_type, keys=tags, sort=search_filter)

	for i in range(0,len(search_results[unicode('mix_set')][unicode('mixes')])):
		print str(i) + ') ' + search_results[unicode('mix_set')][unicode('mixes')][i][unicode('name')].encode('utf-8')

	print 'Enter mix number:'
	if is_playing:
		is_playing = False
		t.join()
	player.currentMix_json = search_results[unicode('mix_set')][unicode('mixes')][int(raw_input())]

	t = threading.Thread( target = play )
	t.start()

		try:
			while True:
				user_input = str(raw_input("Enter a command: "))
				
				if user_input == "pause":
					toggle_pause = True
				elif user_input == 'next':
					next = True
				elif user_input == 'search':
					break
				elif user_input == 'exit':
					is_playing = False
					t.join()
					import sys
					sys.exit()
				else:
					print "Not a valid command"
		except KeyboardInterrupt:
			is_playing = False
			t.join()
			import sys
			sys.exit()













