#include <stdio.h>
#include "HelloJni.h"

/* 该方法在 HelloJni.h 中声明
    JNIEXPORT 和 JNICALL 都是 JNI 中的关键字
    JNIEnv 对应 java 线程中调用的 JNI 环境，通过这个参数可以调用一些JNI 函数
    jobject 对应当前 java 线程中调用本地方法的对象
*/
JNIEXPORT void JNICALL Java_HelloJni_sayHello
(JNIEnv * env, jobject obj)
{
    printf("HelloJni! This is my first jni call.");
}
