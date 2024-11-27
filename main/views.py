from rest_framework import generics, status
from .models import ImageData
from .serializers import ImageDataSerializer
import requests
from .utils import calculate_md5, calculate_phash
from rest_framework.exceptions import APIException
from rest_framework.response import Response


from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
import requests

class ImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = ImageData.objects.all()
    serializer_class = ImageDataSerializer

    def perform_create(self, serializer):
        image_url = serializer.validated_data['image_url']

        try:
            # Fetch the image
            response = requests.get(image_url, timeout=5)
            if response.status_code != 200:
                raise APIException(f"Error: The image URL returned a status code {response.status_code}.")
            
            image_bytes = response.content
            # Compute MD5 and pHash
            md5_hash = calculate_md5(image_bytes)
            phash = calculate_phash(image_bytes) 
            
            # Save the image data with MD5 and pHash
            image_data = serializer.save(md5_hash=md5_hash, phash=phash)

            # Add the success response after saving
            return Response(
                {"message": "Image URL created successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            raise APIException(f"Error processing the image: {str(e)}")

class ImageRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = ImageData.objects.all()
    serializer_class = ImageDataSerializer

    def perform_update(self, serializer):
        try:
            if 'image_url' in serializer.validated_data:
                image_url = serializer.validated_data['image_url']
                # Re-fetch the image and re-compute MD5, pHash if the image URL changes
                response = requests.get(image_url, timeout=5)
                if response.status_code == 200:
                    image_bytes = response.content
                    md5_hash = calculate_md5(image_bytes)
                    phash = calculate_phash(image_bytes)
                    # Update the instance with new values
                    serializer.save(md5_hash=md5_hash, phash=phash)
                else:
                    raise APIException(f"Error: The image URL returned a status code {response.status_code}.")
            else:
                serializer.save()

            # Return a success message 
            return Response(
                {"message": "Image updated successfully.", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class ImageDeleteAPIView(generics.DestroyAPIView):
    queryset = ImageData.objects.all()
    serializer_class = ImageDataSerializer
    def destroy(self, request, *args, **kwargs):
        image_data = self.get_object()
        image_data.delete()
        return Response(
            {'message': 'Image deleted successfully.'}, 
            status=status.HTTP_204_NO_CONTENT
        )
