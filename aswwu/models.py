# models.py

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
import uuid
import datetime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import hashlib
from pattern.en import pluralize

# create a UUID generator function
def uuid_gen():
    return str(uuid.uuid4())

# define a base model for all other models
class Base(object):
    @declared_attr
    def __tablename__(cls):
        # every model will have a corresponding table that is the lowercase and pluralized version of it's name
        return pluralize(cls.__name__.lower())

    # every model should also have an ID as a primary key
    # as well as a column indicated when the data was last updated
    id = Column(String(50), primary_key=True, default=uuid_gen)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    # a useful function is being able to call `model.to_json()` and getting valid JSON to send to the user
    def to_json(self, **kwargs):
        obj = {}
        # get the column names of the table
        columns = [str(key).split(".")[1] for key in self.__table__.columns]
        # if called with `model.to_json(skipList=["something"])`
        # then "something" will be added to the list of columns to skip
        skipList = ['id'] + kwargs.get('skipList', [])
        # if called similarly to skipList, then only those columns will even be checked
        # by default we check all of the table's columns
        limitList = kwargs.get('limitList', columns)
        for key in limitList:
            if key not in skipList:
                # fancy way of saying "self.key"
                value = getattr(self, key)
                # try to set the value as a string, but that doesn't always work
                # NOTE: this should be encoded more properly sometime
                try:
                    obj[key] = str(value)
                except Exception as e:
                    pass
        return obj

# assign our Base class to SQLAlchemy
Base = declarative_base(cls=Base)

# you guessed it, our generic User model
class User(Base):
    wwuid = Column(String(7), unique=True)
    username = Column(String(250), nullable=False)
    full_name = Column(String(250))
    status = Column(String(250))
    roles = Column(String(500))

# table for profile data
class Profile(Base):
    wwuid = Column(String(7), ForeignKey('users.wwuid'), nullable=False)
    username = Column(String(250))
    full_name = Column(String(250))
    photo = Column(String(250))
    gender = Column(String(250))
    birthday = Column(String(250))
    email = Column(String(250))
    phone = Column(String(250))
    website = Column(String(250))
    majors = Column(String(500))
    minors = Column(String(500))
    graduate = Column(String(250))
    preprofessional = Column(String(250))
    class_standing = Column(String(250))
    high_school = Column(String(250))
    class_of = Column(String(250))
    relationship_status = Column(String(250))
    attached_to = Column(String(250))
    quote = Column(String(1000))
    quote_author = Column(String(250))
    hobbies = Column(String(500))
    career_goals = Column(String(1000))
    favorite_books = Column(String(1000))
    favorite_food = Column(String(1000))
    favorite_movies = Column(String(1000))
    favorite_music = Column(String(1000))
    pet_peeves = Column(String(500))
    personality = Column(String(250))
    views = Column(Integer)
    privacy = Column(Integer)
    department = Column(String(250))
    office = Column(String(250))
    office_hours = Column(String(250))

    # sometimes useful to only get a small amount of information about a user
    # e.g. listing ALL of the profiles in a cache for faster search later
    def base_info(self):
        return self.to_json(limitList=['username', 'full_name', 'photo', 'email', 'views'])

# an unfortunately large table to hold the volunteer information
# NOTE: this should and could probably be stored as a JSON blob
class Volunteer(Base):
    wwuid = Column(String(7), ForeignKey('users.wwuid'), nullable=False)
    campus_ministries = Column(Boolean, default=False)
    student_missions = Column(Boolean, default=False)
    aswwu = Column(Boolean, default=False)
    circle_church = Column(Boolean, default=False)
    university_church = Column(Boolean, default=False)
    buddy_program = Column(Boolean, default=False)
    assist = Column(Boolean, default=False)
    lead = Column(Boolean, default=False)
    audio_slash_visual = Column(Boolean, default=False)
    health_promotion = Column(Boolean, default=False)
    construction_experience = Column(Boolean, default=False)
    outdoor_slash_camping = Column(Boolean, default=False)
    concert_assistance = Column(Boolean, default=False)
    event_set_up = Column(Boolean, default=False)
    children_ministries = Column(Boolean, default=False)
    children_story = Column(Boolean, default=False)
    art_poetry_slash_painting_slash_sculpting = Column(Boolean, default=False)
    organizing_events = Column(Boolean, default=False)
    organizing_worship_opportunities = Column(Boolean, default=False)
    organizing_community_outreach = Column(Boolean, default=False)
    bible_study = Column(Boolean, default=False)
    wycliffe_bible_translator_representative = Column(Boolean, default=False)
    food_preparation = Column(Boolean, default=False)
    graphic_design = Column(Boolean, default=False)
    poems_slash_spoken_word = Column(Boolean, default=False)
    prayer_team_slash_prayer_house = Column(Boolean, default=False)
    dorm_encouragement_and_assisting_chaplains = Column(Boolean, default=False)
    scripture_reading = Column(Boolean, default=False)
    speaking = Column(Boolean, default=False)
    videography = Column(Boolean, default=False)
    drama = Column(Boolean, default=False)
    public_school_outreach = Column(Boolean, default=False)
    retirement_slash_nursing_home_outreach = Column(Boolean, default=False)
    helping_the_homeless_slash_disadvantaged = Column(Boolean, default=False)
    working_with_youth = Column(Boolean, default=False)
    working_with_children = Column(Boolean, default=False)
    greeting = Column(Boolean, default=False)
    shofar_for_vespers = Column(Boolean, default=False)
    music = Column(String(250), default=False)
    join_small_groups = Column(Boolean, default=False)
    lead_small_groups = Column(Boolean, default=False)
    can_transport_things = Column(Boolean, default=False)
    languages = Column(String(250), default=False)
    wants_to_be_involved = Column(Boolean, default=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    # for easier admin searching, show only the fields that aren't false or blank
    def only_true(self):
        fields = ['campus_ministries','student_missions','aswwu','circle_church','university_church','assist','lead','audio_slash_visual','health_promotion','construction_experience','outdoor_slash_camping','concert_assistance','event_set_up','children_ministries','children_story','art_poetry_slash_painting_slash_sculpting','organizing_events','organizing_worship_opportunities','organizing_community_outreach','bible_study','wycliffe_bible_translator_representative','food_preparation','graphic_design','poems_slash_spoken_word','prayer_team_slash_prayer_house','dorm_encouragement_and_assisting_chaplains','scripture_reading','speaking','videography','drama','public_school_outreach','retirement_slash_nursing_home_outreach','helping_the_homeless_slash_disadvantaged','working_with_youth','working_with_children','greeting','shofar_for_vespers','music','join_small_groups','lead_small_groups','can_transport_things','languages','wants_to_be_involved']
        data = []
        for f in fields:
            if getattr(self, f) == True:
                data.append(str(f))
            elif getattr(self, f) != '':
                if f == 'music':
                    data.append({'music': self.music})
                elif f == 'languages':
                    data.append({'languages': self.languages})
        return data

class ElectionBase(object):
    @declared_attr
    def __tablename__(cls):
        # every model will have a corresponding table that is the lowercase and pluralized version of it's name
        return pluralize(cls.__name__.lower())

    # every model should also have an ID as a primary key
    # as well as a column indicated when the data was last updated
    id = Column(String(50), primary_key=True, default=uuid_gen)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    # a useful function is being able to call `model.to_json()` and getting valid JSON to send to the user
    def to_json(self, **kwargs):
        obj = {}
        # get the column names of the table
        columns = [str(key).split(".")[1] for key in self.__table__.columns]
        # if called with `model.to_json(skipList=["something"])`
        # then "something" will be added to the list of columns to skip
        skipList = ['id'] + kwargs.get('skipList', [])
        # if called similarly to skipList, then only those columns will even be checked
        # by default we check all of the table's columns
        limitList = kwargs.get('limitList', columns)
        for key in limitList:
            if key not in skipList:
                # fancy way of saying "self.key"
                value = getattr(self, key)
                # try to set the value as a string, but that doesn't always work
                # NOTE: this should be encoded more properly sometime
                try:
                    obj[key] = str(value)
                except Exception as e:
                    pass
        return obj

ElectionBase = declarative_base(cls=ElectionBase)

class User(ElectionBase):
    wwuid = Column(String(7), unique=True)
    username = Column(String(250), nullable=False)
    full_name = Column(String(250))
    status = Column(String(250))
    roles = Column(String(500))

class Election(ElectionBase):
    wwuid = Column(String(7), ForeignKey('users.wwuid'), nullable=False)
    candidate_one = Column(String(50))
    candidate_two = Column(String(50))
    sm_one = Column(String(50))
    sm_two = Column(String(50))
    new_department = Column(String(150))
    district = Column(String(50))
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    #return those who have voted
    def voters(self):
        return self.to_json(limitList=['wwuid'])

    def base_info(self):
        return self.to_json(limitList=['wwuid', 'updated_at'])

    def info(self):
        return self.to_json(limitList=['wwuid','candidate_one','candidate_two','sm_one','sm_two','new_department','updated_at'])

# NOTE: this class is no longer in use, but it's left here for posterity
# class CollegianArticle(Base):
#     __tablename__ = "collegian_articles"
#     id = Column(String(50), primary_key=True, default=uuid_gen)
#     volume = Column(Integer, nullable=False)
#     issue = Column(Integer, nullable=False)
#     title = Column(String(500), nullable=False)
#     author = Column(String(500), nullable=False)
#     section = Column(String(500), nullable=False)
#     content = Column(Text, nullable=False)
#     updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
#     def to_json(self):
#         return {'id': str(self.id), 'volume': str(self.volume), 'issue': str(self.issue), 'title': str(self.title), 'author': str(self.author), 'section': str(self.section), 'content': self.content.encode('utf-8', 'ignore'), 'updated_at': str(self.updated_at)}
