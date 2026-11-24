import pandas as pd
from sklearn.datasets import load_iris                # 붓꽃 데이터 세트
from sklearn.model_selection import train_test_split  # 데이터 분할
from sklearn.neighbors import KNeighborsClassifier    # K-최근접 이웃 알고리즘 모델

iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target)
print("원본 데이터 미리보기 (특징 X)\n", X.head())
print("원본 데이터 미리보기(목표 변수 y)\n", y.head())

print("원본 데이터 미리보기 (특징 X)\n", X.tail())
print("원본 데이터 미리보기(목표 변수 y)\n", y.tail())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                    random_state=42, stratify=y)
# print(f" - 훈련 데이터 형태: {X_train.shape}, {y_train.shape}")
# print(f" - 테스트 데이터 형태: {X_test.shape}, {y_test.shape}")

# knn_model = KNeighborsClassifier(n_neighbors=5)
# knn_model.fit(X_train, y_train)

# y_pred = knn_model.predict(X_test)
# print(y_pred[:5])                 # 예측 결과 중 앞의 5개만 출력
# print(y_test[:5])    
