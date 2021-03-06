
from nintendo.nex import common
import enum

import logging
logger = logging.getLogger(__name__)


class Gathering(common.Structure):
	def __init__(self, id, owner_pid, host_pid, player_min, player_max,
				 participation_policy, policy_argument, flags, state, description):
		self.id = id
		self.owner_pid = owner_pid
		self.host_pid = host_pid
		self.player_min = player_min
		self.player_max = player_max
		self.participation_policy = participation_policy
		self.policy_argument = policy_argument
		self.flags = flags
		self.state = state
		self.description = description
		
	def get_name(self):
		return "Gathering"
	
	def save(self, stream):
		stream.u32(self.id)
		stream.u32(self.owner_pid)
		stream.u32(self.host_pid)
		stream.u16(self.player_min)
		stream.u16(self.player_max)
		stream.u32(self.participation_policy)
		stream.u32(self.policy_argument)
		stream.u32(self.flags)
		stream.u32(self.state)
		stream.string(self.description)
		
	def load(self, stream):
		self.id = stream.u32()
		self.owner_pid = stream.u32()
		self.host_pid = stream.u32()
		self.player_min = stream.u16()
		self.player_max = stream.u16()
		self.participation_policy = stream.u32()
		self.policy_argument = stream.u32()
		self.flags = stream.u32()
		self.state = stream.u32()
		self.description = stream.string()
common.DataHolder.register(Gathering, "Gathering")


class MatchmakeSystem(enum.IntEnum):
	GLOBAL = 1
	FRIENDS = 2


class MatchmakeSessionSearchCriteria(common.Structure):
	def __init__(self, attribs, game_mode, min_players, max_players, matchmake_system, vacant_only,
				 exclude_locked, exclude_non_host_pid, selection_method, vacant_participants=None):
		self.attribs = attribs
		self.game_mode = game_mode
		self.min_players = min_players
		self.max_players = max_players
		self.matchmake_system = matchmake_system
		self.vacant_only = vacant_only
		self.exclude_locked = exclude_locked
		self.exclude_non_host_pid = exclude_non_host_pid
		self.selection_method = selection_method
		self.vacant_participants = vacant_participants
	
	def save(self, stream):
		stream.list(self.attribs, stream.string)
		stream.string(self.game_mode)
		stream.string(self.min_participants)
		stream.string(self.max_participants)
		stream.string(self.matchmake_system)
		stream.bool(self.vacant_only)
		stream.bool(self.exclude_locked)
		stream.bool(self.exclude_non_host_pid)
		stream.u32(self.selection_method)
		
		if self.version >= 0:
			stream.u16(self.vacant_participants)
		
		
class MatchmakeSession(Gathering):
	def __init__(self, id, owner_pid, host_pid, player_min, player_max,
				 participation_policy, policy_argument, flags, state,
				 description, game_mode, attribs, open_participation,
				 matchmake_system, application_data, player_count,
				 session_key, progress_score=None, option=None):
		super().__init__(
			id, owner_pid, host_pid, player_min, player_max,
			participation_policy, policy_argument, flags, state,
			description
		)
		self.game_mode = game_mode
		self.attribs = attribs
		self.open_participation = open_participation
		self.matchmake_system = matchmake_system
		self.application_data = application_data
		self.player_count = player_count
		self.session_key = session_key
		self.progress_score = progress_score
		self.option = option

	def get_name(self):
		return "MatchmakeSession"

	def save(self, stream):
		stream.u32(self.game_mode)
		stream.list(self.attribs, stream.u32)
		stream.bool(self.open_participation)
		stream.u32(self.matchmake_system)
		stream.buffer(self.application_data)
		stream.u32(self.player_count)
		if self.version >= 0:
			stream.u8(self.progress_score)
		stream.buffer(self.session_key)
		if self.version >= 0:
			stream.u32(self.option)
		
	def load(self, stream):
		self.game_mode = stream.u32()
		self.attribs = stream.list(stream.u32)
		self.open_participation = stream.bool()
		self.matchmake_system = stream.u32()
		self.application_data = stream.buffer()
		self.player_count = stream.u32()
		if self.version >= 0:
			self.progress_score = stream.u8()
		self.session_key = stream.buffer()
		if self.version >= 0:
			self.option = stream.u32()
common.DataHolder.register(MatchmakeSession, "MatchmakeSession")


class SimplePlayingSession(common.Structure):
	def load(self, stream):
		self.pid = stream.uint()
		self.gid = stream.u32()
		self.game_mode = stream.u32()
		self.attribute = stream.u32()
		
		
class PlayingSession(common.Structure):
	def load(self, stream):
		self.pid = stream.uint()
		self.gathering = stream.anydata()


class MatchMakingClient:

	METHOD_REGISTER_GATHERING = 1
	METHOD_UNREGISTER_GATHERING = 2
	METHOD_UNREGISTER_GATHERINGS = 3
	METHOD_UPDATE_GATHERING = 4
	METHOD_INVITE = 5
	METHOD_ACCEPT_INVITATION = 6
	METHOD_DECLINE_INVITATION = 7
	METHOD_CANCEL_INVITATION = 8
	METHOD_GET_INVITATIONS_SENT = 9
	METHOD_GET_INVITATIONS_RECEIVED = 10
	METHOD_PARTICIPATE = 11
	METHOD_CANCEL_PARTICIPATION = 12
	METHOD_GET_PARTICIPANTS = 13
	METHOD_ADD_PARTICIPANTS = 14
	METHOD_GET_DETAILED_PARTICIPANTS = 15
	METHOD_GET_PARTICIPANTS_URLS = 16
	METHOD_FIND_BY_TYPE = 17
	METHOD_FIND_BY_DESCRIPTION = 18
	METHOD_FIND_BY_DESCRIPTION_REGEX = 19
	METHOD_FIND_BY_ID = 20
	METHOD_FIND_BY_SINGLE_ID = 21
	METHOD_FIND_BY_OWNER = 22
	METHOD_FIND_BY_PARTICIPANTS = 23
	METHOD_FIND_INVITATIONS = 24
	METHOD_FIND_BY_SQL_QUERY = 25
	METHOD_LAUNCH_SESSION = 26
	METHOD_UPDATE_SESSION_URL = 27
	METHOD_GET_SESSION_URL = 28
	METHOD_GET_STATE = 29
	METHOD_SET_STATE = 30
	METHOD_REPORT_STATS = 31
	METHOD_GET_STATS = 32
	METHOD_DELETE_GATHERING = 33
	METHOD_GET_PENDING_DELETIONS = 34
	METHOD_DELETE_FROM_DELETIONS = 35
	METHOD_MIGRATE_GATHERING_OWNERSHIP = 36
	METHOD_FIND_BY_DESCRIPTION_LIKE = 37
	METHOD_REGISTER_LOCAL_URL = 38
	METHOD_REGISTER_LOCAL_URLS = 39
	METHOD_UPDATE_SESSION_HOST = 40
	METHOD_GET_SESSION_URLS = 41
	METHOD_UPDATE_SESSION_HOST = 42

	PROTOCOL_ID = 0x15

	def __init__(self, backend):
		self.client = backend.secure_client
		
	def find_by_sql_query(self, query, result_range):
		logger.info("MatchMaking.find_by_sql_query(%s, [%i, %i])", query, result_range.offset, result_range.size)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_FIND_BY_SQL_QUERY)
		stream.string(query)
		stream.add(result_range)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		gatherings = stream.list(stream.anydata)
		logger.info("MatchMaking.find_by_sql_query -> %i results", len(gatherings))
		return gatherings
		
	def get_session_url(self, gid):
		logger.info("MatchMaking.get_session_url(%08X)", gid)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_SESSION_URL)
		stream.u32(gid)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		result = stream.bool()
		url = stream.string()
		logger.info("MatchMaking.get_session_url -> (%i, %s)", result, url)
		return result, url
		
	def get_session_urls(self, gid):
		logger.info("MatchMaking.get_session_urls(%08X)", gid)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_SESSION_URLS)
		stream.u32(gid)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		urls = stream.list(stream.stationurl)
		logger.info("MatchMaking.get_session_urls -> %s", urls)
		return urls


class MatchmakeExtensionClient:
	
	METHOD_CLOSE_PARTICIPATION = 1
	METHOD_OPEN_PARTICIPATION = 2
	METHOD_AUTO_MATCHMAKE_POSTPONE = 3
	METHOD_BROWSE_MATCHMAKE_SESSION = 4
	METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS = 5
	METHOD_CREATE_MATCHMAKE_SESSION = 6
	METHOD_JOIN_MATCHMAKE_SESSION = 7
	METHOD_MODIFY_CURRENT_GAME_ATTRIBUTE = 8
	METHOD_UPDATE_NOTIFICATION_DATA = 9
	METHOD_GET_FRIEND_NOTIFICATION_DATA = 10
	METHOD_UPDATE_APPLICATION_BUFFER = 11
	METHOD_UPDATE_MATCHMAKE_SESSION_ATTRIBUTE = 12
	METHOD_GETLST_FRIEND_NOTIFICATION_DATA = 13
	METHOD_UPDATE_MATCHMAKE_SESSION = 14
	METHOD_AUTO_MATCHMAKE_WITH_SEARCH_CRITERIA_POSTPONE = 15
	METHOD_GET_PLAYING_SESSION = 16
	METHOD_CREATE_COMMUNITY = 17
	METHOD_UDPATE_COMMUNITY = 18
	METHOD_JOIN_COMMUNITY = 19
	METHOD_FIND_COMMUNITY_BY_GATHERING_ID = 20
	METHOD_FIND_OFFICIAL_COMMUNITY = 21
	METHOD_FIND_COMMUNITY_BY_PARTICIPANT = 22
	METHOD_UPDATE_PRIVACY_SETTING = 23
	METHOD_GET_MY_BLACK_LIST = 24
	METHOD_ADD_TO_BLACK_LIST = 25
	METHOD_REMOVE_FROM_BLACK_LIST = 26
	METHOD_CLEAR_MY_BLACK_LIST = 27
	METHOD_REPORT_VIOLATION = 28
	METHOD_IS_VIOLATION_USER = 29
	METHOD_JOIN_MATCHMAKE_SESSION_EX = 30
	METHOD_GET_SIMPLE_PLAYING_SESSION = 31
	METHOD_GET_SIMPLE_COMMUNITY = 32
	METHOD_AUTO_MATCHMAKE_WITH_GATHERING_ID_POSTPONE = 33
	METHOD_UPDATE_PROGRESS_SCORE = 34
	METHOD_DEBUG_NOTIFY_EVENT = 35
	METHOD_GENERATE_MATCHMAKE_SESSION_SYSTEM_PASSWORD = 36
	METHOD_CLEAR_MATCHMAKE_SESSION_SYSTEM_PASSWORD = 37
	METHOD_CREATE_MATCHMAKE_SESSION_WITH_PARAM = 38
	METHOD_JOIN_MATCHMAKE_SESSION_WITH_PARAM = 39
	METHOD_AUTO_MATCHMAKE_WITH_PARAM_POSTPONE = 40
	METHOD_FIND_MATCHMAKE_SESSION_BY_GATHERING_ID_DETAIL = 41
	METHOD_BROWSER_MATCHMAKE_SESSION_NO_HOLDER = 42
	METHOD_BROWSE_MATCHMAKE_SESSION_WITH_HOST_URLS_NO_HOLDER = 43
	METHOD_UPDATE_MATCHMAKE_SESSION_PART = 44
	METHOD_REQUEST_MATCHMAKING = 45
	METHOD_WITHDRAW_MATCHMAKING = 46
	METHOD_WITHDRAW_MATCHMAKING_ALL = 47
	
	PROTOCOL_ID = 0x6D
	
	def __init__(self, backend):
		self.backend = backend
		self.client = backend.secure_client
		
	def auto_matchmake(self, gathering, message):
		logger.info("MatchmakeExtension.auto_matchmake(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_POSTPONE)
		stream.anydata(gathering)
		stream.string(message)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		object = stream.anydata()
		logger.info("MatchmakeExtension.auto_matchmake -> %s", object.get_name())
		return object
		
	def create_matchmake_session(self, gathering, description, player_count):
		logger.info("MatchmakeExtension.create_matchmake_session(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_CREATE_MATCHMAKE_SESSION)
		stream.anydata(gathering)
		stream.string(description)
		stream.u16(player_count)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		gid = stream.u32()
		session_key = stream.buffer()
		logger.info("MatchmakeExtension.create_matchmake_session -> (%08X, %s)", gid, session_key.hex())
		return gid, session_key
		
	def join_matchmake_session(self, gid, message):
		logger.info("MatchmakeExtension.join_matchmake_session(%i, %s)", gid, message)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_JOIN_MATCHMAKE_SESSION)
		stream.u32(gid)
		stream.string(message)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		session_key = stream.buffer()
		logger.info("MatchmakeExtension.join_matchmake_session -> %s", session_key.hex())
		return session_key
		
	#This seems to be the method that's used by most games
	def auto_matchmake_with_search_criteria(self, search_criteria, gathering, message):
		logger.info("MatchmakeExtension.auto_matchmake_with_search_criteria(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_AUTO_MATCHMAKE_WITH_SEARCH_CRITERIA_POSTPONE)
		stream.list(search_criteria, stream.add)
		stream.anydata(gathering)
		stream.string(message)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		object = stream.anydata()
		logger.info("MatchmakeExtension.auto_matchmake_with_search_criteria -> %s", object.get_name())
		return object
		
	def get_playing_session(self, pids):
		logger.info("MatchmakeExtension.get_playing_session(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_PLAYING_SESSION)
		stream.list(pids, stream.uint)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		sessions = stream.list(PlayingSession)
		logger.info("MatchmakeExtension.get_playing_session -> done")
		return sessions

	def get_simple_playing_session(self, pids, include_login_user):
		logger.info("MatchmakeExtension.get_simple_playing_session(...)")
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_GET_SIMPLE_PLAYING_SESSION)
		stream.list(pids, stream.uint)
		stream.bool(include_login_user)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		sessions = stream.list(SimplePlayingSession)
		logger.info("MatchmakeExtension.get_simple_playing_session -> done")
		return sessions

	def find_matchmake_session_by_gid_detail(self, gid):
		logger.info("MatchmakeExtension.find_matchmake_session_by_gid_detail(%08X)", gid)
		#--- request ---
		stream, call_id = self.client.init_request(self.PROTOCOL_ID, self.METHOD_FIND_MATCHMAKE_SESSION_BY_gid_DETAIL)
		stream.u32(gid)
		self.client.send_message(stream)
		
		#--- response ---
		stream = self.client.get_response(call_id)
		session = stream.extract(MatchmakeSession)
		logger.info("MatchmakeExtension.find_matchmake_session_by_gid_detail -> done")
		return session
