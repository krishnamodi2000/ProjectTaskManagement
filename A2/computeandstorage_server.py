import grpc
from concurrent import futures
import computeandstorage_pb2
import computeandstorage_pb2_grpc
import boto3

s3_bucket_name = "computeandstoragekrishnam"

# Create a class to implement the gRPC server
class EC2OperationsServicer(computeandstorage_pb2_grpc.EC2OperationsServicer):
    def StoreData(self, request, context):
        # Retrieve the data from the request message
        data = request.data

        # Generate a unique filename or key for the S3 object
        filename = "fileB00931943.txt"

        # Create an S3 client using boto3
        s3_client = boto3.client("s3")
        # Upload the data to S3 
        # Reference : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object.html
        s3_client.put_object(
            Body=data,
            Bucket=s3_bucket_name,
            Key=filename
        )

        # Create the publicly readable URL for the uploaded file on S3
        s3uri = f"https://{s3_bucket_name}.s3.amazonaws.com/{filename}"

        # Return the publicly readable URL for the created file on S3
        return computeandstorage_pb2.StoreReply(s3uri=s3uri)

    def AppendData(self, request, context):
        # Retrieve the data from the request message
        data = request.data

        filename = "fileB00931943.txt"
        # Create an S3 client using boto3
        s3_client = boto3.client("s3")

        # Get the existing object from S3
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=filename)
        existing_data = response["Body"].read().decode()

        # Append the new data to the existing data
        updated_data = existing_data + data

        # Overwrite the existing object with the updated data
        s3_client.put_object(
            Body=updated_data,
            Bucket=s3_bucket_name,
            Key=filename
        )

        return computeandstorage_pb2.AppendReply()

    def DeleteFile(self, request, context):
        # Retrieve the S3 URI from the request message
        s3uri = request.s3uri


        parts = s3uri.replace("https://", "").split("/")
        bucket_name = parts[0].split(".")[0]  # Extract the bucket name without the domain
        object_key = "/".join(parts[1:])
        print(bucket_name, object_key, flush=True)
        # Create an S3 client using boto3
        s3_client = boto3.client("s3")

        # Delete the file from S3
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)

        return computeandstorage_pb2.DeleteReply()

# Create a gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())

    # Add the servicer class to the server
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(
        EC2OperationsServicer(), server
    )

    # Start the server on port 50051 (change if needed)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
