# Docker Setup cho DRR Project

## Yêu cầu
- Docker
- Docker Compose

## Cách sử dụng

### 1. Khởi động container

```bash
docker compose up -d --build
```

Container sẽ chạy ở chế độ background và giữ cho container luôn hoạt động.

### 2. Tạo thư mục models (nếu chưa có)

```bash
mkdir models
```

### 3. Truy cập vào container

```bash
docker exec -it drr_model bash
```

### 4. Chạy lệnh trong container

Sau khi vào container, bạn có thể chạy các lệnh thủ công:

#### Training Models:

**DRR-Base (model_type=0):**
```bash
python main.py --train true --train_set dataset/rec_train_set.sample.txt --validation_set dataset/rec_validation_set.sample.txt --model_type 0 --batch_size 128 --train_epochs 50 --train_steps_per_epoch 10 --validation_steps 15 --early_stop_patience 5 --lr_per_step 1000 --d_model 128 --d_inner_hid 256 --saved_model_name models/drr_model_0.h5
```

**DRR-Personalized-v1 (model_type=1):**
```bash
python main.py --train true --train_set dataset/rec_train_set.sample.txt --validation_set dataset/rec_validation_set.sample.txt --model_type 1 --batch_size 128 --train_epochs 50 --train_steps_per_epoch 10 --validation_steps 15 --early_stop_patience 5 --lr_per_step 1000 --d_model 128 --d_inner_hid 256 --saved_model_name models/drr_model_1.h5
```

**DRR-Personalized-v2 (model_type=2):**
```bash
python main.py --train true --train_set dataset/rec_train_set.sample.txt --validation_set dataset/rec_validation_set.sample.txt --model_type 2 --batch_size 128 --train_epochs 50 --train_steps_per_epoch 10 --validation_steps 15 --early_stop_patience 5 --lr_per_step 1000 --d_feature 19 --d_model 128 --d_inner_hid 256 --saved_model_name models/drr_model_2.h5
```

#### Testing Models:

**DRR-Base:**
```bash
python main.py --test_set dataset/rec_test_set.sample.txt --batch_size 2 --model_type 0 --saved_model_name models/drr_model_0.h5 --d_model 128 --d_inner_hid 256
```

**DRR-Personalized-v1:**
```bash
python main.py --test_set dataset/rec_test_set.sample.txt --batch_size 2 --model_type 1 --saved_model_name models/drr_model_1.h5 --d_model 128 --d_inner_hid 256
```

**DRR-Personalized-v2:**
```bash
python main.py --test_set dataset/rec_test_set.sample.txt --batch_size 2 --model_type 2 --saved_model_name models/drr_model_2.h5 --d_feature 19 --d_model 128 --d_inner_hid 256
```

#### Đánh giá Metrics:

```bash
python metric.py dataset/rec_test_set.sample.txt.predict.out
```

### 5. Thoát khỏi container

```bash
exit
```

### 6. Dừng và xóa container

```bash
docker compose down
```

## Lệnh hữu ích

```bash
# Xem logs của container
docker logs drr_model

# Xem logs realtime
docker logs -f drr_model

# Restart container
docker compose restart

# Rebuild và restart
docker compose up -d --build

# Xem container đang chạy
docker ps
```

## Parameters Giải thích

- `--train`: true để training, false hoặc bỏ qua để test
- `--model_type`: Loại model (0=base, 1=personalized-v1, 2=personalized-v2)
- `--batch_size`: Batch size cho training/testing
- `--train_epochs`: Số epochs training
- `--train_steps_per_epoch`: Số steps mỗi epoch
- `--validation_steps`: Số steps validation
- `--early_stop_patience`: Số epochs chờ trước khi early stop
- `--lr_per_step`: Update learning rate mỗi X steps
- `--d_feature`: Feature dimension (12 cho base/v1, 19 cho v2)
- `--saved_model_name`: Tên file model sẽ save

## Cấu trúc thư mục

```
drr/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── dataset/           # Mounted từ host
│   ├── rec_train_set.sample.txt
│   ├── rec_validation_set.sample.txt
│   └── rec_test_set.sample.txt
├── models/            # Mounted từ host - chứa trained models
├── log/               # Mounted từ host - chứa TensorBoard logs
├── drr_model.py
├── main.py
└── metric.py
```

## Lưu ý

- Container sử dụng TensorFlow 1.15.5 (tương thích với code)
- Đã fix Python 2 → Python 3 compatibility
- Volumes được mount từ host để dữ liệu không mất khi restart container
- Container chạy ở background, dùng `docker exec -it drr_model bash` để vào

## Tham khảo

Paper: "Personalized Re-ranking for E-commerce Recommendation Systems"
