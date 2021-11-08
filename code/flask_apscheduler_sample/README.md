# Flask APScheduler Sample

---

# Story

基於工作上的經驗，需要建立一個類似非同步的功能/資料流模式。

當功能已知需要花費大量時間執行(例如需要執行1分鐘)，若按照原有的設計模式，
當 User request data 到後端後，後端需要處理1分鐘，User就必須得等待1分鐘才能到response，
這種運作方式基本上是不行的，會為使用者帶來奇差無比的使用體驗。

---

# Think

因此需要設計一種工作排程方式，當後端接到任務後，
後端會先回應User 201 代表收到需求，之後再建立Background execution任務來執行耗時工作，
最後User 再去(例如DB 或可儲存任務結果)的功能取得運行結果

---

:::danger
:-1: 不好的示範
:::
```sequence
User->API Service: data
API Service->FuncA:  data
FuncA-->FuncA: Processing\n 10 minutes...
Note left of User: User: Wait 10 minutes...
FuncA->API Service: Return Result
API Service-->User: Return Result
```
![](https://i.imgur.com/f0W6VWc.png)

---

:::info
:accept: 可行的解決辦法的示範
:::

```sequence
User->API Service: data
API Service-->User: We will start\n as soon as possible (201)
API Service->FuncA:  data
FuncA-->FuncA: Processing\n 10 minutes...
FuncA-->API Service: Return Result
API Service->DB or storage: Save Result
```

```sequence
User->API Service: Please give me the results
API Service->DB or storage: Query execution results
DB or storage-->API Service: Return Result
API Service-->User: Return Result
```

![](https://i.imgur.com/hDxKOo4.png)