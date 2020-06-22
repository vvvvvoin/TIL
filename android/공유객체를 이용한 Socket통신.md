#### 공유객체를 이용한 Socket통신

- 공유객체를 통해 Socket통신이 이루어짐
- 서버에 요청을 보낼때 공유객체를 통해 전달되기에 서버에 무분별한 데이터를 넘기지 않는다



- Main.java
```java
    Thread thread = new Thread(new Runnable() {
        @Override
        public void run() {
            try {
                socket = new Socket("70.12.60.98", 1357);
                printWriter = new PrintWriter(socket.getOutputStream());

                while (true) {
                    String msg = sharedObject.pop();
                    printWriter.println(msg);
                    printWriter.flush();
                }
            } catch (IOException e) {
                Log.v(TAG, "Socket Communication IOException==" + e);
            }
        }
```
- 메인에 Thread로 socket stream을 열고 공유객체를 통해 메세지를 전달하도록 한다.



- SharedObject.java
```java
public class SharedObject {
    Object monitor = new Object();
    private LinkedList<String> dataList = new LinkedList<>();
    
    public void put(String msg) {
        synchronized (monitor){
            dataList.addLast(msg);
            monitor.notify();
        }
    }
    public String pop() {
        String result = "";
        synchronized (monitor) {
            if (dataList.isEmpty()) {
                try{
                    monitor.wait();
                    result = dataList.removeFirst();
                }catch (InterruptedException e){
                    
                }
            }else {
                result = dataList.removeFirst();
            }
        }
        return result;
    }
}
```
- 공유객체에서는 LinkedList에 전달된 메세지가 저장된다
- 더이상 LinkedList에 꺼낼 데이터가 없으면 wait()을 통해 대기
- 다른 클래스로 부터 데이터가 put()되면 notofify()를 통해 다시 데이터를 pop()하여 메세지 전달

