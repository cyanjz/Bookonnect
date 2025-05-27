# BooKonnect

### Project 설정 - Backend
- numpy의 경우 호환성 문제로 인해 requirements에 작성할 경우 문제가 발생하여 별도로 install 해주셔야 합니다!
1. pjt venv setup
```bash
pyhton -m venv venv
source venv/Scripts/Activate
pip install -r requirements.txt
pip install numpy
```
2. pjt load data
```bash
python manage.py migrate
python manage.py loaddata books.json
python manage.py loaddata accounts.json
```

### Project 설정 - Frontend
```bash
npm install
npm run dev
```

<br/>

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

<br/>

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

<br/>

## III. ERD & Figma
- ERD : [dbdiagram.io](https://dbdiagram.io/d/BooKonnect-682d89d5b9f7446da3781e24)
- Mockup : [Figma - Mockup](https://www.figma.com/design/KOCRExKa4dtO6s1nEGjOuw/UI-UX-Design?node-id=28-2127&t=wRG9Xoe8DMNUYKqY-1)
- Vue Component Design : [Figma - Vue Design](https://www.figma.com/board/3OZRecDrvzWPQshV8xvya0/Vue-Design?node-id=0-1&t=5wAuDjYbcsEQZY8Z-1)

<br/>

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

<br/>

## V. 핵심 기능
### 생성형 AI
1. 쓰레드 내용 문법 검사 및 변경 사항을 사용자가 취사 선택할 수 있는 기능.
2. 쓰레드 생성시 내용을 기반으로 배너 이미지 생성.
3. 도서 설명 Embedding 기반 도서 추천. IV. 항목 참조.

### SNS 기능
1. 쓰레드 및 댓글 CRUD.
2. 쓰레드 및 댓글에 대한 좋아요 기능 구현.
3. Follow 기능 구현.

<br/>

## VI. 생성형 AI 활용
### Vue template
Vue template의 prototype을 만드는데 생성형 AI를 적극 활용. 미리 만들어 두었던 mockup 이미지와 사용할 json 형태의 데이터를 전달하여 vue template 코드를 생성. 생성된 코드를 기반으로 기능을 구현, 수정.

### Django rest auth
Django rest auth에서 User model customization에 생성형 AI를 활용, 코드의 대략적인 형태를 확인. 이후 생성형 AI에서 검색 키워드에 대한 힌트를 얻어 추가적인 검색을 통해 dj-rest-auth에서 User model 및 serializer의 customization 수행.

### Vue async
Vue에서 작업하면서 비동기에 대한 이해가 부족하여 해당 과정이 완료되기 전 많은 에러가 발생. 특히, undefined error가 많이 발생했는데, 원인을 생성형 AI를 통해 파악하고, 코드를 수정. isLoading 변수를 선언하고 v-if를 통해 axios 요청이 완료되었을 때 template를 rendering 하도록 함.

<br/>

## VII. 기타
### 안재혁
Python을 활용하여 django backend를 구축하는 것은 빠르게 완료할 수 있었지만, vue 및 js에 대한 숙련도가 부족하여 Frontend 구축 및 디버깅에 오랜 시간이 걸렸습니다. axios가 비동기로 처리되어 js script의 일반적인 흐름과 다르게 동작하다 보니 undefined 및 null로 인한 오류가 많이 발생했습니다. 처음에는 해당 버그들의 원인을 몰라 console.log로 매번 확인을 해야했으나, 프로젝트가 마무리되어 가는 지금은 버그 메시지의 일반적인 원인에 대한 감을 잡아서 vue 및 frontend에서의 개발 시간을 단축할 수 있을 것 같습니다.

### 김채은
지금까지 해왔던 관통프로젝트를 그대로 적용 및 사용하면 될 것이라고 생각했는데, 처음부터 무에서 유를 창조하려고 하니까 생각보다 복잡했고 그래서 더 어려웠던 것 같습니다. 실제 프로젝트를 진행하면서 django 및 js와 vue에 대한 학습 및 숙련도가 많이 부족했음을 알게 되었고, 페어 그리고 프로젝트 자체에서도 정말 많은 것을 배울 수 있었습니다.

특히 이론을 배울 때는 개념들이 서로 어떻게 연계되는지, 왜 이렇게 하는지 몰랐던 것들을 직접 웹 사이트를 제작해보면서 이해를 하고 공부할 수 있는 시간이 됐습니다. 또한, git을 통해 협업하는 것을 경험해봤는데, 마냥 어렵기만 하던 git 사용이 생각보다 재미있고 쉬움을 알게 되었고, 왜 개발자들이 github을 이용하는지 몸소 느낄 수 있었습니다.

콘솔 창을 봐가면서 디버깅하는 것도 많이 배웠습니다. 그 전에는 콘솔 창을 봐야하는 것을 알아도 어떤 부분을 봐야하고, 보더라도 어떤 의미인지 한번에 파악하는 것이 힘들었는데, 프로젝트를 진행하며서 어떤 식으로 해야하는지 감을 잡게 된 것 같습니다.

그리고 무엇보다, 어려웠어도 만드는 것 자체가 너무 재미있었습니다. 직접 해보니 힘들어도 느끼고 배우는 것이 많았고, 시간이 부족한 것을 떠나 제가 좀 더 잘하는 사람이었다면 더 재미있게 할 수 있었을 것 같습니다. (느리고 부족한 페어를 잘 이끌어주고 가르쳐준 페어에게 감사 인사 올립니다..ㅎㅎㅎ)