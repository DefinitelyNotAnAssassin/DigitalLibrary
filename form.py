from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, SelectField)
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileRequired, FileField, FileAllowed
import uuid



class CourseForm(FlaskForm):
  Bookname = StringField('Bookname',validators =[InputRequired(), Length(min=10, max=100)])
  Author = StringField('Author', validators = [InputRequired(), Length(min=10, max=100)])
  Category = SelectField('Category', validators = [InputRequired()], choices =['General Works, Computer Science & Information','Philosophy & Psychology', 'Religion', "Social Sciences", "Language", "Science", "Technology","Arts & Recreation", "Literature", "History & Geography"])
  Filename = StringField('Filename', validators=[InputRequired()])
  File = FileField('File', validators=[FileRequired(), FileAllowed(['.pdf', 'pdf'], "PDF Files Only")])
  
  
class SearchForm(FlaskForm):
  Bookname = StringField('Bookname',validators =[InputRequired(), Length(min=10, max=100)])
  Category = SelectField('Category', validators = [InputRequired()], choices =['General Works, Computer Science & Information','Philosophy & Psychology', 'Religion', "Social Sciences", "Language", "Science", "Technology","Arts & Recreation", "Literature", "History & Geography"])

  