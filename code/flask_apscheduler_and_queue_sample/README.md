# Flask APScheduler And Queue Sample

---

# Story

基於Flask APScheduler Sample改良，建立一個Queue機制，並依照資源需求，
建立指定的Worker數量，定時處理Queue裡的任務。

---

# Think

建立一個Queue機制
後端會先回應User 201 代表收到需求，需求會先Put in Queue，
背景正在執行的Worker會定時去Queue要任務來執行。
最後User 再去(例如DB 或可儲存任務結果)的功能取得運行結果

:::info
:accept: 可行的解決辦法的示範
:::

```sequence
User->API Service: data
API Service-->User: We will start\n as soon as possible (201)
API Service->Queue: Put Data
FuncA-->Queue: Get Data
Queue->FuncA: Return Data
FuncA-->FuncA: Processing\n 10 minutes...
FuncA-->DB or storage: Return Result
```

```sequence
User->API Service: Please give me the results
API Service->DB or storage: Query execution results
DB or storage-->API Service: Return Result
API Service-->User: Return Result
```

![](https://i.imgur.com/E5nnELV.png)