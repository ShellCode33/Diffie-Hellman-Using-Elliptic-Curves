# Elliptic Curves Cryptography
Simple Python script showing how to implement Diffie Hellman and El Gamal algorithms using elliptic curves

## Diffie Hellman

You can run the Server and the Client to see that the generated secret key is the same on both sides.

```
shellcode@laptop:/home/shellcode/Crypto/EllipticCurves  $ ./Server.py
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 1x + 442
Which curve do you want to use ? [default 1] : 
Invalid curve id. Default will be used.
Client connected.
Received parameter:  (446, 107)
sha1(secret_key) = c6996b0e4bcdd51d3d8229273662e0f865dd5d87
```

```
shellcode@laptop:/home/shellcode/Crypto/EllipticCurves  $ ./Client.py
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 1x + 442
Which curve do you want to use ? [default 1] : 
Invalid curve id. Default will be used.
Received parameter:  (180, 115)
sha1(secret_key) = c6996b0e4bcdd51d3d8229273662e0f865dd5d87
```


## El Gamal

## More

You can add more elliptic curves inside the class EllipticCurve :
