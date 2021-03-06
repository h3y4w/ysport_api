from flask_restful import Resource, request
import DB
from response import ResponseAPI
  
class Videos (Resource):
    def get(self, id):
        data = {} 
        error = False 
        message = "" 

        try:
            video = DB.Video.find_model_by_id(id)
            if video is not None:
                data = video.json() 
                data['views'] = video.get_views(only_count=True)
                print data

        except Exception as e:
            error = True
            message = str(e)
            DB.session.rollback()

        finally:
            return ResponseAPI('get', 'Videos', data=data, error=error, message=message).json()
  
    def put(self, id):
    # Edits Video information
        error = False
        message = None
    
    
        try:
            video = DB.Video.find_model_by_id(id)
            video.title = request.args.get('title') or video.title
            video.text = request.args.get('text') or video.text
            DB.save()
          
        except Exception as e:
            DB.session.rollback()
            error = True
            message = str(e)
          
        finally:
            return ResponseAPI('put', 'Videos', message=message, error=error).json()




class Video (Resource):
    def post(self):
      #Creates video
      
        error = None
        message = None
        data = None

        try:
            params = request.get_json(force=True)
            params['user_id']=1
            data = DB.Video.create(params).json()
    
        except Exception as e:
            DB.session.rollback()
            error = True
            message = str(e)
        
        finally:
            return ResponseAPI('post', 'Video', message=message, error=error, data=data).json()
        

