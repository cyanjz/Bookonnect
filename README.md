# BooKonnect

## I. 임무 분담
### 김채은
- UI / UX Design
- Frontend design
- Frontend dev
- Frontend styling
- ERD
### 안재혁
- UI/UX Design
- Frontend dev
- Backend dev
- Data preprocessing

## II. 목표 서비스 및 실제 구현 정도
### 구현 완료 사항
- Aladin API를 사용하여 도서 정보 preprocessing 및 DB 구축
- Thread, Comment CURD
- Thread, Comment Like & User Follow
- OpenAI API를 활용한 쓰레드 내용 리뷰
- OpenAI API를 활용한 쓰레드 배너 이미지 생성.
- Embedding vector를 활용한 도서 추천.
### 미구현 사항
- Social login
- Book collection CRUD (사용자가 만드는 도서 묶음)
- Following user의 thread 목록 보기.

## III. ERD & Figma
- ERD : [dbdiagram.io](https://dbdiagram.io/d/BooKonnect-682d89d5b9f7446da3781e24)
- Mockup : [Figma - Mockup](https://www.figma.com/design/KOCRExKa4dtO6s1nEGjOuw/UI-UX-Design?node-id=28-2127&t=wRG9Xoe8DMNUYKqY-1)
- Vue Component Design : [Figma - Vue Design](https://www.figma.com/board/3OZRecDrvzWPQshV8xvya0/Vue-Design?node-id=0-1&t=5wAuDjYbcsEQZY8Z-1)

## IV. 도서 추천 알고리즘.
### 1. OpenAI API를 사용한 embedding vector 생성 및 저장
- OpenAI API를 사용하여 book_description에 대한 embedding vector를 생성하고 DB에 저장한다.
```python
def update_embedding():
    books = Book.objects.all()
    ai_instance = OpenAiAPI()
    for book in books:
        # embedding update
        description = book.book_description
        if description == '':
            pass
        else:
            result = ai_instance.get_description_embedding([description])
            result = [item.embedding for item in result]
            book.book_embedding = result[0]
            book.save()
```
### 2. User Thread 기반 User 선호도 벡터 계산
- Thread의 별점을 가중치로 사용자의 선호도 벡터를 계산.
- 계산된 vector를 기반으로 도서 리스트를 정렬하고, 상위 10개를 추출하여 추천.
```python
# views.py의 일부분.
user = request.user
# thread 별로 작성된 점수로 weighted avg 계산
threads = user.thread_set.all()
total_weights = 0
embedding = None
if user.thread_set.count() != 0:
    for thread in threads:
        weight = thread.thread_book_review_rank + 1
        raw_embedding = thread.book.book_embedding
        if raw_embedding:
            temp = np.array(json.loads(raw_embedding))
            if embedding is None:
                embedding = weight * temp
            else:
                embedding = np.add(embedding, weight * temp)
            total_weights += weight
    if total_weights == 0:
        print('유효한 embedding이 없습니다...')
        books = get_list_or_404(Book)
        serializer = BookListSerializer(books, many=True)
        sorted_data = sorted(serializer.data, key=lambda x: x['book_customer_review_rank'])
        resp = {
            'data': sorted_data,
            'success': False,
        }
        return Response(resp)
```

## V. 핵심 기능
### 생성형 AI
1. 쓰레드 내용 문법 검사 및 변경 사항을 사용자가 취사 선택할 수 있는 기능.
2. 쓰레드 생성시 내용을 기반으로 배너 이미지 생성.
3. 도서 설명 Embedding 기반 도서 추천. IV. 항목 참조.

### SNS 기능
1. 쓰레드 및 댓글 CRUD.
2. 쓰레드 및 댓글에 대한 좋아요 기능 구현.
3. Follow 기능 구현.

## VI. 생성형 AI 활용
### Vue template
Vue template의 prototype을 만드는데 생성형 AI를 적극 활용. 미리 만들어 두었던 mockup 이미지와 사용할 json 형태의 데이터를 전달하여 vue template 코드를 생성. 생성된 코드를 기반으로 기능을 구현, 수정.

### Django rest auth
Django rest auth에서 User model customization에 생성형 AI를 활용, 코드의 대략적인 형태를 확인. 이후 생성형 AI에서 검색 키워드에 대한 힌트를 얻어 추가적인 검색을 통해 dj-rest-auth에서 User model 및 serializer의 customization 수행.

### Vue async
Vue에서 작업하면서 비동기에 대한 이해가 부족하여 해당 과정이 완료되기 전 많은 에러가 발생. 특히, undefined error가 많이 발생했는데, 원인을 생성형 AI를 통해 파악하고, 코드를 수정. isLoading 변수를 선언하고 v-if를 통해 axios 요청이 완료되었을 때 template를 rendering 하도록 함.

## VII. 기타
### 안재혁
Python을 활용하여 django backend를 구축하는 것은 빠르게 완료할 수 있었지만, vue 및 js에 대한 숙련도가 부족하여 Frontend 구축 및 디버깅에 오랜 시간이 걸렸습니다. axios가 비동기로 처리되어 js script의 일반적인 흐름과 다르게 동작하다 보니 undefined 및 null로 인한 오류가 많이 발생했습니다. 처음에는 해당 버그들의 원인을 몰라 console.log로 매번 확인을 해야했으나, 프로젝트가 마무리되어 가는 지금은 버그 메시지의 일반적인 원인에 대한 감을 잡아서 vue 및 frontend에서의 개발 시간을 단축할 수 있을 것 같습니다.