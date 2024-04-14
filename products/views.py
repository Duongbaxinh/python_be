from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth import get_user_model
from django.http import Http404
from .serializers import CategorySerializer,ProductSerializer,ProductCommentSerializer,ProductImageSerializer,ProductImageSerializer,InventorySerializer,CartSerializer
from .models import Category,Product,ProductImage,ProductComment,Inventory,Cart
from rest_framework.parsers import JSONParser
from json import JSONDecodeError
from ecommerce.helpers import custom_response, parse_request
from user.models import UserAccount


User = get_user_model()


def index(request):
    return render(request, 'index.html')
# Create your views here.
class CategoryAPIView(views.APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            print('run at here ........................... ')
            categories = Category.objects.all()
            serializer = CategorySerializer(categories,many = True)
            return custom_response('Get all categories successfully!', 'Success', serializer.data, 200)
        except Exception as e:
           print('error::::: ',e)
           return custom_response('Get all categories failed!', 'Error', None, 400)
    
    def post(self,request):
        data = parse_request(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return custom_response('Create category successfully!', 'Success', serializer.data, 201)
        else:
            return custom_response('Create category failed', 'Error', serializer.errors, 400)

class CategoryDetailAPIView(views.APIView):
    permission_classes = [AllowAny]
    def get_object(self, id_slug):
        try:
            return Category.objects.get(id=id_slug)
        except:
            raise Http404

    def get(self, request, id_slug, format=None):
        try:
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category)
            return custom_response('Get category successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get category failed!', 'Error', "Category not found!", 400)

    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update category successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update category failed', 'Error', serializer.errors, 400)
        except:
                return custom_response('Update category failed', 'Error', "Category not found!", 400)
                
    def delete(self, request, id_slug):
        try:
            category = self.get_object(id_slug)
            category.delete()
            return custom_response('Delete category successfully!', 'Success', {"category_id": id_slug},204)
        except:
            return custom_response('Delete category failed!', 'Error', "Category not found!", 400)
        
class ProductViewAPI(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            products = Product.objects.all()
            serializers = ProductSerializer(products, many=True)
            return custom_response('Get all products successfully!', 'Success', serializers.data, 200)
        except Exception as e :
            print(e)
            return custom_response('Get all products failed!', 'Error', None, 400)
    def post(self, request):
        try:
                data = parse_request(request)
                # product có ràng buộc phải có một category_id nên phải query tìm category đó trước
                category = Category.objects.get(id=data['category_id'])
                product = Product(
                product_name=data['product_name'],
                # unit=data['unit'],
                product_price=data['product_price'],
                discount=data['discount'],
                amount=data['amount'],
                product_rate= data['product_rate'],
                product_brand= data['product_brand'],
                product_genuine = data['product_genuine'],
                product_best = data['product_best'],
                is_public=data['is_public'],
                product_thumbnail=data['product_thumbnail'],
                # gán category đã tìm được vào field category_id
                category_id=category
                )
                            
                product.save()
                serializer = ProductSerializer(product)
                return custom_response('Create product successfully!', 'Success', serializer.data, 201)
        except Exception as e:
                return custom_response('Create product failed', 'Error', {"error": str(e)}, 400)

class ProductDetailAPIView(views.APIView):
    permission_classes = [AllowAny]
    def get_object(self, id_slug):
        try:
            return Product.objects.get(id=id_slug)
        except:
            raise Http404
    def get(self, request, id_slug, format=None):
        try:
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product)
            return custom_response('Get product successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product failed!', 'Error', "Product not found!", 400)

    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product failed', 'Error', "Category not found!", 400)
    def delete(self, request, id_slug):
        try:
            product = self.get_object(id_slug)
            product.delete()
            return custom_response('Delete product successfully!', 'Success', {"product_id": id_slug}, 204)
        except:
            return custom_response('Delete product failed!', 'Error', "Product not found!", 400)

class ProductInventoryAPIView(views.APIView):
    permission_classes = [AllowAny]
    def put(self,request,id_slug):
        data = parse_request(request)
    
        product = Product.objects.get(id = id_slug)
        print('check id slug ::: 9999 ',data, '-----',id_slug)
        # if(product.DoesNotExist):
        #     return custom_response('Get product failed!', 'Error', "Product not found22!", 400)
        inven = Inventory.objects.get(inven_product = id_slug)
        if(inven.inven_amount < 0 and data['type'] == 'up'):
          return custom_response('Product run out of!', 'Error', "Product run out of!", 400)
        serializer = InventorySerializer(inven)
        return custom_response('Check out product!','Success',serializer.data,200)


class ProductCategoryAPIView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request, id_slug, format=None):
        print("check slug id :::: ", id_slug)
        try:
            category = Category.objects.get(id = id_slug)
            # if(category.DoesNotExist):
            #     raise custom_response('Get product failed!', 'Error', "Product not found!", 400)
            products = Product.objects.filter(category_id=id_slug)
            print('check product',products)
            serializer = ProductSerializer(products,many = True)
            return custom_response('Get product successfully!', 'Success', serializer.data, 200)
        except Exception as e:
            print('check error::::: ', e)
            return custom_response('Get product failed!', 'Error', "Product not found!", 400)

class ProductImageAPIView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request, product_id_slug):
        try:
            product_images = ProductImage.objects.filter(product_id=product_id_slug).all()
            serializers = ProductImageSerializer(product_images, many=True)
            return custom_response('Get all product images successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product images failed!', 'Error', 'Product images not found',400)

    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            product_image = ProductImage(
            product_id=product,
            image_url=data['image_url']
            )
            product_image.save()
            serializer = ProductImageSerializer(product_image)
            return custom_response('Create product image successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product image failed', 'Error', {"error": str(e)}, 400)

class ProductImageDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return ProductImage.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductImage.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            category = Category.objects.get(id = id_slug)
            if(category.DoesNotExist):
                return ustom_response('Get category failed!', 'Error', "Category not found!", 400)
            product_image = self.get_object(id_slug)
            serializer = ProductImageSerializer(product_image)
            return custom_response('Get product image successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product image failed!', 'Error', "Product image not found!", 400)
    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_image = self.get_object_with_product_id(product_id_slug, id_slug)
            serializer = ProductImageSerializer(product_image, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product image successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product image failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product image failed', 'Error', "Product image not found!", 400)
    def delete(self, request, product_id_slug, id_slug):
        try:
            product_image = self.get_object_with_product_id(product_id_slug, id_slug)
            product_image.delete()
            return custom_response('Delete product image successfully!', 'Success', {"product_image_id":
            id_slug}, 204)
        except:
            return custom_response('Delete product image failed!', 'Error', "Product image not found!",400)

class ProductCommentAPIView(views.APIView):
    def get(self, request, product_id_slug):
            try:
                product_comments = ProductComment.objects.filter(product_id=product_id_slug).all()
                serializers = ProductCommentSerializer(product_comments, many=True)
                return custom_response('Get all product comments successfully!', 'Success', serializers.data,
                200)
            except:
                return custom_response('Get all product comments failed!', 'Error', None, 400)

    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            user = User.objects.get(id=data['user_id'])
            product_comment = ProductComment(
            product_id=product,
            rating=data['rating'],
            comment=data['comment'],
            user_id=user,
            parent_id=data['parent_id']
            )
            product_comment.save()
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Create product comment successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product comment failed', 'Error', {"error": str(e)}, 400)

class ProductCommentDetailAPIView(views.APIView):
    def get_object(self, id_slug):
        try:
            return ProductComment.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductComment.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_comment = self.get_object(id_slug)
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Get product comment successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product comment failed!', 'Error', "Product comment not found!",
            400)

    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_comment = self.get_object_with_product_id(product_id_slug, id_slug)
            serializer = ProductCommentSerializer(product_comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product comment successfully!', 'Success', serializer.data,
                200)
            else:
                return custom_response('Update product comment failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product comment failed', 'Error', "Product comment not found!", 400)

    def delete(self, request, product_id_slug, id_slug):
        try:
            product_comment = self.get_object_with_product_id(product_id_slug, id_slug)
            product_comment.delete()
            return custom_response('Delete product comment successfully!', 'Success',
            {"product_comment_id": id_slug},
            204)
        except:
            return custom_response('Delete product comment failed!', 'Error', "Product comment not       found!", 400)


class CartAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            idUser = request.user.id
            print("run at here")
            carts = Cart.objects.filter(user_id=idUser)
            serializers = CartSerializer(carts, many=True)
            return custom_response('Get all categories successfully!', 'Success', serializers.data, 200)
        except Exception as e:
            return custom_response('Get all categories failed!', 'Error', None, 400)
    def post(self, request):
        idUser = request.user.id
        try:
            data = parse_request(request)
            print('check data value 3333333:::: ',data)
            product = Product.objects.get(id=data['prid'])
            print('checkkkkkkkkkkkkkkkkkkkkkkkkkkkk :::::: ', product)
            user = UserAccount.objects.get(id=idUser)
            print('checkkkkkkkkkkkkkkkkkkkkkkkkkkkk22 :::::: ', user)
            cart = Cart(
            product_id= product,
            quantity_count=data['quantity_count'],
            user_id=user
            )
            cart.save()
            serializer = CartSerializer(cart)
            return custom_response('Create Cart successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            print('check create Cart :::: ', e)
            return custom_response('Create Cart failed!', 'Error', [str(e)], 400)
    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            cart = Cart.objects.get(id = id_slug)
            serializer = CartSerializer(cart, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update cart successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update cart failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update cart failed', 'Error', "Category not found!", 400)

class cartDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, id_slug):
        try:
            return Cart.objects.get(id=id_slug)
        except:
            raise Http404
    def get(self, request, id_slug, format=None):
        try:
            cart = self.get_object(id_slug)
            serializer = CartSerializer(cart)
            return custom_response('Get cart successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get cart failed!', 'Error', "cart not found!", 400)

    def put(self, request, id_cart):
        try:
            print('run at here :::: 0001')
            data = parse_request(request)
            cart = Cart.objects.get(id = id_cart)
            if data['type'] == 'up':
                cart.quantity_count = cart.quantity_count + 1
            else: 
                cart.quantity_count = cart.quantity_count - 1
            cart.save()
            serializer = CartSerializer(cart)
            return custom_response('Update cart successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Update cart failed', 'Error', "Category not found!", 400)
    def delete(self, request, id_cart):
        print('dd;',id_cart)
        try:
            cart = Cart.objects.get(id = id_cart)
            cart.delete()
            return custom_response('Delete cart successfully!', 'Success', {"cart_id": id_cart}, 204)
        except Exception as e:
            print(e)
            return custom_response('Delete cart failed!', 'Error', "cart not found!", 400)
