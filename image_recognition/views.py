from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from .utils import face_match
import tempfile
import base64
from .models import UserImageEmbeddings
import pickle


class Index(View):
    def get(self, request):
        template_name = 'index.html'
        return render(request, template_name)
    
    def post(self, request):
        person_name = request.POST.get('personName')
        img_content = base64.b64decode(request.POST['img'].split(',')[1])
        tfl = tempfile.NamedTemporaryFile(delete=True)
        tfl.write(img_content)
        img = face_match.cv2.imread(tfl.name)
        tfl.close()
        if person_name:
            faces = face_match.getFace(img)
            if faces:
                face = faces[0]
                embedding = face['embedding']
                UserImageEmbeddings.objects.create(person_name=person_name, image_embedding=pickle.dumps(embedding))
                return HttpResponse("Image stored.")
            else:
                return HttpResponse("No face detected.")
        else:
            faces = face_match.getFace(img)
            if faces:
                face = faces[0]
                embedding = face['embedding']
            
                uies = UserImageEmbeddings.objects.all()
                for row in uies:
                    dist = face_match.compare2face(pickle.loads(row.image_embedding), embedding)
                    if dist < 1.10:
                        return HttpResponse(row.person_name)
            else:
                return HttpResponse("No face detected.")
        
        return HttpResponse("Match not found.")


