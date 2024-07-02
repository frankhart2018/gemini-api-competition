import * as Minio from "minio";


export class MinioClient {
    constructor() {
        this.minioClient = new Minio.Client({
            endPoint: process.env.MINIO_ENDPOINT,
            port: 9000,
            useSSL: false,
            accessKey: process.env.MINIO_ACCESS_KEY,
            secretKey: process.env.MINIO_SECRET_KEY
        });
    }

    makeBucketIfNotExists = async (bucketName) => {
        const exists = await this.minioClient.bucketExists(bucketName);

        if (!exists) {
            await this.minioClient.makeBucket(bucketName);
        }
    }

    uploadFile = async (bucketName, sourceFilePath, destFilePath, fileType) => {
        const metaData = {
            "Content-Type": fileType
        };

        await this.makeBucketIfNotExists(bucketName);
        await this.minioClient.fPutObject(bucketName, destFilePath, sourceFilePath, metaData);
    }

    uploadFileIfNotExists = async (bucketName, sourceFilePath, destFilePath, fileType) => {
        await this.makeBucketIfNotExists(bucketName);
        this.minioClient.statObject(bucketName, destFilePath, async (err, _) => {
            if (err) {
                await this.uploadFile(bucketName, sourceFilePath, destFilePath, fileType);
            }
        });
    }

    downloadFile = async (bucketName, filePath, localDownloadPath) => {
        await this.minioClient.fGetObject(bucketName, filePath, localDownloadPath);
    }
}