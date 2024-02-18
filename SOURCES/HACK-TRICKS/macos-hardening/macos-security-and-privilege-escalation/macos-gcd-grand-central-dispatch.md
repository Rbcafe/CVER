# macOS GCD - Grand Central Dispatch

<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>

## Basic Information

**Grand Central Dispatch (GCD),** also known as **libdispatch**, is available in both macOS and iOS. It's a technology developed by Apple to optimize application support for concurrent (multithreaded) execution on multicore hardware.

**GCD** provides and manages **FIFO queues** to which your application can **submit tasks** in the form of **block objects**. Blocks submitted to dispatch queues are **executed on a pool of threads** fully managed by the system. GCD automatically creates threads for executing the tasks in the dispatch queues and schedules those tasks to run on the available cores.

{% hint style="success" %}
In summary, to execute code in **parallel**, processes can send **blocks of code to GCD**, which will take care of their execution. Therefore, processes don't create new threads; **GCD executes the given code with its own pool of threads**.
{% endhint %}

This is very helpful to manage parallel execution successfully, greatly reducing the number of threads processes create and optimising the parallel execution. This is idea for tasks that require **great parallelism** (brute-forcing?) or for tasks that shouldn't block the main thread: For example, the main thread on iOS handles UI interactions, so any other functionality that could make the app hang (searching, accessing a web, reading a file...) is managed this way.

## Objective-C

In Objetive-C there are different functions to send a block to be executed in parallel:

* [**dispatch\_async**](https://developer.apple.com/documentation/dispatch/1453057-dispatch\_async): Submits a block for asynchronous execution on a dispatch queue and returns immediately.
* [**dispatch\_sync**](https://developer.apple.com/documentation/dispatch/1452870-dispatch\_sync): Submits a block object for execution and returns after that block finishes executing.
* [**dispatch\_once**](https://developer.apple.com/documentation/dispatch/1447169-dispatch\_once): Executes a block object only once for the lifetime of an application.
* [**dispatch\_async\_and\_wait**](https://developer.apple.com/documentation/dispatch/3191901-dispatch\_async\_and\_wait): Submits a work item for execution and returns only after it finishes executing. Unlike [**`dispatch_sync`**](https://developer.apple.com/documentation/dispatch/1452870-dispatch\_sync), this function respects all attributes of the queue when it executes the block.

These functions expect these parameters: [**`dispatch_queue_t`**](https://developer.apple.com/documentation/dispatch/dispatch\_queue\_t) **`queue,`** [**`dispatch_block_t`**](https://developer.apple.com/documentation/dispatch/dispatch\_block\_t) **`block`**

This is the **struct of a Block**:

```c
struct Block {
   void *isa; // NSConcreteStackBlock,...
   int flags;
   int reserved;
   void *invoke;
   struct BlockDescriptor *descriptor;
   // captured variables go here
};
```

And this is an example to use **parallelism** with **`dispatch_async`**:

```objectivec
#import <Foundation/Foundation.h>

// Define a block
void (^backgroundTask)(void) = ^{
    // Code to be executed in the background
    for (int i = 0; i < 10; i++) {
        NSLog(@"Background task %d", i);
        sleep(1);  // Simulate a long-running task
    }
};

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        // Create a dispatch queue
        dispatch_queue_t backgroundQueue = dispatch_queue_create("com.example.backgroundQueue", NULL);
        
        // Submit the block to the queue for asynchronous execution
        dispatch_async(backgroundQueue, backgroundTask);
        
        // Continue with other work on the main queue or thread
        for (int i = 0; i < 10; i++) {
            NSLog(@"Main task %d", i);
            sleep(1);  // Simulate a long-running task
        }
    }
    return 0;
}
```

## Swift

**`libswiftDispatch`** is a library that provides **Swift bindings** to the Grand Central Dispatch (GCD) framework which is originally written in C.\
The **`libswiftDispatch`** library wraps the C GCD APIs in a more Swift-friendly interface, making it easier and more intuitive for Swift developers to work with GCD.

* **`DispatchQueue.global().sync{ ... }`**
* **`DispatchQueue.global().async{ ... }`**
* **`let onceToken = DispatchOnce(); onceToken.perform { ... }`**
* **`async await`**
  * **`var (data, response) = await URLSession.shared.data(from: URL(string: "https://api.example.com/getData"))`**

**Code example**:

```swift
import Foundation

// Define a closure (the Swift equivalent of a block)
let backgroundTask: () -> Void = {
    for i in 0..<10 {
        print("Background task \(i)")
        sleep(1)  // Simulate a long-running task
    }
}

// Entry point
autoreleasepool {
    // Create a dispatch queue
    let backgroundQueue = DispatchQueue(label: "com.example.backgroundQueue")
    
    // Submit the closure to the queue for asynchronous execution
    backgroundQueue.async(execute: backgroundTask)
    
    // Continue with other work on the main queue
    for i in 0..<10 {
        print("Main task \(i)")
        sleep(1)  // Simulate a long-running task
    }
}
```

## Frida

The following Frida script can be used to **hook into several `dispatch`** functions and extract the queue name, the backtrace and the block: [**https://github.com/seemoo-lab/frida-scripts/blob/main/scripts/libdispatch.js**](https://github.com/seemoo-lab/frida-scripts/blob/main/scripts/libdispatch.js)

```bash
frida -U <prog_name> -l libdispatch.js

dispatch_sync
Calling queue: com.apple.UIKit._UIReusePool.reuseSetAccess
Callback function: 0x19e3a6488 UIKitCore!__26-[_UIReusePool addObject:]_block_invoke
Backtrace:
0x19e3a6460 UIKitCore!-[_UIReusePool addObject:]
0x19e3a5db8 UIKitCore!-[UIGraphicsRenderer _enqueueContextForReuse:]
0x19e3a57fc UIKitCore!+[UIGraphicsRenderer _destroyCGContext:withRenderer:]
[...]
```

## Ghidra

Currently Ghidra doesn't understand neither the ObjectiveC **`dispatch_block_t`** structure, neither the **`swift_dispatch_block`** one.

So if you want it to understand them, you could just **declare them**:

<figure><img src="../../.gitbook/assets/image (688).png" alt="" width="563"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (690).png" alt="" width="563"><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (691).png" alt="" width="563"><figcaption></figcaption></figure>

Then, find a place in the code where they are **used**:

{% hint style="success" %}
Note all of references made to "block" to understand how you could figure out that the struct is being used.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (692).png" alt="" width="563"><figcaption></figcaption></figure>

Right click on the variable -> Retype Variable and select in this case **`swift_dispatch_block`**:

<figure><img src="../../.gitbook/assets/image (693).png" alt="" width="563"><figcaption></figcaption></figure>

Ghidra will automatically rewrite everything:

<figure><img src="../../.gitbook/assets/image (694).png" alt="" width="563"><figcaption></figcaption></figure>

<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>
