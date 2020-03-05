# Elliptic Curves Cryptography
Simple Python module implementing Diffie Hellman, El Gamal and DSA algorithms using elliptic curves.
These algorithms don't guarentee authentication, a MITM attack could be performed in order to hijack the public key.

Just stating the obvious here : those scripts are for educational purposes only, do not use it in anything serious.

## Diffie Hellman

You can run the server then the client to see the generated secret key is the same on both sides.

```
shellcode@laptop:/home/shellcode/Crypto/Elliptic-Curves-Algorithms/demo  git:(master*) $ ./server_dh.py 
Waiting for client...
Client connected.
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 109454571331697278617670725030735128145969349647868738157201323556196022393856x + 107744541122042688792155207242782455150382764043089114141096634497567301547839
Which curve do you want to use ? [default 1] : 2
DH remote parameter:  (97138913127608459681135738238509448998881853099266326240818802819815727419427, 81448349606468118554919636307944551532799340194696086176081536871720747880178)
sha1(secret_key) = 0dcbd6505d31db24dc58da473788560c4e2c0c0a
```

```
shellcode@laptop:/home/shellcode/Crypto/Elliptic-Curves-Algorithms/demo  git:(master*) $ ./client_dh.py 
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 109454571331697278617670725030735128145969349647868738157201323556196022393856x + 107744541122042688792155207242782455150382764043089114141096634497567301547839
Which curve do you want to use ? [default 1] : 2
Received parameter:  (101031615897151406461415691397072605734385577084318901325540546750227921865334, 27542374492052082156151997086209450249676378539960817158152497875354487990941)
sha1(secret_key) = 0dcbd6505d31db24dc58da473788560c4e2c0c0a

```


## El Gamal
This algorithm enables you to exchange encrypted messages asymetrically :

```
shellcode@laptop:/home/shellcode/Crypto/Elliptic-Curves-Algorithms/demo  git:(master*) $ ./server_eg.py 
Waiting for client...
Client connected.
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 109454571331697278617670725030735128145969349647868738157201323556196022393856x + 107744541122042688792155207242782455150382764043089114141096634497567301547839
Which curve do you want to use ? [default 1] : 2
Sending public key to client...
Cipher received: ((36773955846380952537541287416321290092702887872322771572617991430614752831531, 44933767436387503989913507543382489164051634957543418839767485102168306626167), (70407540337237980970268132682638014818491496697688582317136440105096786225421, 61756750508062620281767048328228541891853280587433946972746014997795360954962))
Received: (82638672503301278923015998535776227331280144783487139112686874194432446389503, 43992510890276411535679659957604584722077886330284298232193264058442323471611)
```

```
shellcode@laptop:/home/shellcode/Crypto/Elliptic-Curves-Algorithms/demo  git:(master*) $ ./client_eg.py 
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 109454571331697278617670725030735128145969349647868738157201323556196022393856x + 107744541122042688792155207242782455150382764043089114141096634497567301547839
Which curve do you want to use ? [default 1] : 2
Server's public key received.
Sending encrypted message to server...
```

## DSA
This algorithm enables you to sign messages in order to check integrity, to be sure the message is from a legitimate emitter.

```
shellcode@laptop:/home/shellcode/Crypto/Elliptic-Curves-Algorithms/demo  git:(master*) $ ./server_dsa.py 
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 109454571331697278617670725030735128145969349647868738157201323556196022393856x + 107744541122042688792155207242782455150382764043089114141096634497567301547839
Which curve do you want to use ? [default 1] : 2
Waiting for client...
Client connected.
Public key is sent.
Signature is sent.
```

```
shellcode@laptop:/home/shellcode/Crypto/Elliptic-Curves-Algorithms/demo  git:(master*) $ ./client_dsa.py 
-------------------------------------
1: y² = x³ + 1x + 3
2: y² = x³ + 109454571331697278617670725030735128145969349647868738157201323556196022393856x + 107744541122042688792155207242782455150382764043089114141096634497567301547839
Which curve do you want to use ? [default 1] : 2
Received public key:  (15021019540827427930960423889714676004813071951062158447139104086683546669408, 79401835124672877735276056892375637840864613443911033730883544544473821748130)
Received signature: (10784918051478807134560271922891148593921688428015743990310288453562865141549, 4240444791637007411409401138864890210082751360370998026778984045081195792678)
Is the signature valid : True

```

## More

You can add more elliptic curves inside the EllipticCurve class :
![alt EC Curves](https://github.com/ShellCode33/Elliptic-Curves-Algorithms/raw/master/doc/ec_curves.png)
