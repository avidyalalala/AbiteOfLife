public class HelloJni{

    static{
        System.loadLibrary("hellojni");
    }
    
    public static void main(String[] args){
        HelloJni helloJni = new HelloJni();
        helloJni.sayHello();
    }
    
    native void sayHello();
}
