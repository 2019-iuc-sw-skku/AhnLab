ex = ["libc-hihihi.so.1.2.3", "libc-hihihi.so", "libc-jlksdal", "[notso]", "[kk.kkl]", "soso", "libc-kk.so.2"]

for test in ex:
    if test.split(".so")[-1] == "" or ".so." in test:
        print(test)
