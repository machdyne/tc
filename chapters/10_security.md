# Security

A computer is secure when it does what its owner intends and nothing else: its data is read only by those meant to read it, changed only by those meant to change it, and available when it is needed. This chapter describes the threats to those properties and the means of defending against them, of which cryptography is one.

## Threat Models

Securing a computer begins with a **threat model**: what is to be protected, from whom, and at what cost. A personal machine in a home faces different threats from a server on the Internet, and measures that suit one are wasted effort or inadequate for the other. A notebook of private writing needs protection from someone who picks up the machine; a server needs protection from strangers on the network who try every address; a messaging device may need protection from an adversary who records everything sent and can afford to wait.

Most failures are not failures of cryptography. They come from lost or stolen equipment, weak or reused passwords, programs that trust their input, software from an unknown source, and the absence of a copy when something is deleted. The sections below cover these, and then the cryptography on which secure communication depends.

## Physical Access

Whoever holds a machine can do almost anything with it. They can read its storage card in another computer, replace its configuration flash, attach a device to its pins or take it away. A password that locks the screen protects the running session from someone at the keyboard, but not the data on a card that can be removed.

Data that must remain private on a machine that may be lost or stolen is therefore kept **encrypted**, with a key that is not stored beside it. Equipment that matters is kept where others cannot reach it, in the same way as other valuables.

## Passwords and Keys

A password is strong when it cannot be guessed, even by a program that tries millions of possibilities. Length matters more than complexity: a passphrase of five or six unrelated words, chosen at random, is both stronger and easier to remember than a short password of mixed symbols. Each service should have its own password, so that one leak does not open the others.

A well-designed system never stores a password itself. It stores the result of a deliberately slow hash function, described below, applied to the password together with a random value called a **salt**. To check a password, the system applies the same function and compares the results. Someone who copies the stored record must then spend the same effort for every guess, and the salt prevents a guess from being tested against many records at once. A system can also add a delay after each wrong attempt.

Cryptographic **keys** are long random numbers, far too long to remember. They are kept in files or on devices, and are protected as carefully as the data they protect. A key is also backed up as carefully as data, because an encrypted file whose key is lost is lost with it.

## What Cryptography Provides

**Cryptography** is the use of mathematics to protect information. It provides three properties:

- **Confidentiality**: only the intended receiver can read the message.
- **Integrity**: any change to the message is detected.
- **Authentication**: the receiver can be certain who sent it.

Modern cryptography is public. Its methods are published, studied for years by others before they are trusted, and standardized, and only the keys are secret. A method whose security depends on its design being secret cannot be checked, and usually fails once the design becomes known.

## Hash Functions

A **cryptographic hash function** computes a short, fixed-size value, the **hash** or digest, from data of any length. SHA-256, a widely used example, produces 256 bits, usually written as 64 hex digits. A good hash function has three properties: the same data always gives the same hash; any change to the data, even of one bit, gives a completely different hash; and no one can find two different pieces of data with the same hash, or data that produces a given hash.

As a result, a hash serves as a fingerprint. A copy of a file is checked by computing its hash and comparing it with the original's, as described in [Memory and Storage](#memory-and-storage). A program downloaded from elsewhere is checked against the hash its author published. Passwords are stored as hashes, and digital signatures, described below, are made on the hash of a message rather than on the whole message.

## Symmetric Encryption

**Symmetric** encryption uses one secret key both to encrypt and to decrypt. The common methods are AES, a standard since 2001, and ChaCha20, which is faster in software on processors without special instructions for AES. Keys are 128 or 256 bits long. A 128-bit key has 2 to the 128th possible values, so many that trying them all is beyond any computer that could be built.

Encryption alone provides confidentiality, but not integrity: an attacker who cannot read a message may still be able to change it. Current protocols therefore use **authenticated encryption**, which adds a short tag, computed from the message and the key, that the receiver checks before trusting the message. Each message is also encrypted with a **nonce**, a number that must never be used twice with the same key; reusing one can reveal the messages.

Symmetric encryption is fast, but both ends must already share the key, and delivering it to them securely is difficult.

## Public-Key Cryptography

**Public-key** cryptography solves that problem with a pair of keys. The **public key** can be given to anyone, and the matching **private key** is kept secret. The two are related by mathematics that is easy to compute in one direction and, as far as is known, impractical to reverse on present computers: from the private key the public key is calculated in an instant, but recovering the private key from the public one would take longer than the age of the universe. A padlock is a fair comparison: anyone can close an open padlock, but only the holder of its key can open it.

The pair makes two things possible:

- **Key exchange.** Two machines that have not communicated before can agree on a shared secret over an open network, even while others are listening. X25519 is a common method. The shared secret then becomes the key for fast symmetric encryption.
- **Digital signatures.** A message signed with a private key can be checked by anyone with the public key, and no one without the private key can forge the signature. Ed25519 is a common method. Signatures prove who wrote a message, or who published a program, and that it has not been changed since.

Older systems use RSA for both purposes, with much longer keys.

Public keys raise a question of trust: how to know that a public key belongs to the intended person or site. The web relies on **certificates**, which are public keys signed by organizations that browsers are configured to trust. SSH usually asks the user to confirm a server's key the first time and remembers it afterwards. Between people, keys can be compared in person, or their hashes read aloud.

All of this requires computation. On a small processor, the arithmetic of public-key cryptography can take seconds per connection. On an FPGA computer, the slow parts can be given their own circuits in the FPGA, as described in [Systems on a Chip](#systems-on-a-chip).

## Random Numbers

Keys, salts and nonces must be unpredictable. Computers are deterministic, so they gather unpredictability from physical noise, such as the jitter of free-running oscillators, which a **true random number generator** (TRNG) measures. Many chips, including the FPGA designs in this book, contain one. Because physical noise is slow and imperfect, systems usually use it to seed a **cryptographically secure pseudo-random number generator**, an algorithm that produces an unlimited stream of numbers that cannot be predicted without knowing the seed.

A weak random number generator makes keys predictable, and a connection made with such keys shows no outward sign of it. For this reason the source of randomness is among the most important parts of a secure system.

## The One-Time Pad

One method of encryption is unbreakable in principle, however much computing power an attacker has. In the **one-time pad**, each bit of the message is combined by XOR with one bit of a key that is truly random and as long as the message. The receiver, who holds a copy of the same key, applies XOR with it again, which restores the message:

```text
message     01001000      the letter H
key         10110101      random, used once
            --------
encrypted   11111101      message XOR key
key         10110101      the same key
            --------
message     01001000      encrypted XOR key
```

Because every key is equally likely, every message of the same length is an equally likely explanation of the encrypted bits, and the encrypted text reveals nothing but its length. This property is called **information-theoretic security**: it rests on the randomness of the key, not on the difficulty of a calculation.

The guarantee holds only under strict conditions. The key must be truly random, as long as all the messages it will protect, kept secret, and never used twice. If the same key is used for two messages, combining the two encrypted texts cancels the key and leaves the XOR of the two messages, from which both can often be recovered. The key must also be delivered to the receiver in advance, by some means other than the channel it protects. These costs have kept the one-time pad to uses in which the highest security justifies them.

Small, open hardware can make those conditions practical. **Einszeit**, an open-source security device under development at Machdyne and intended to become a product, provides one-time-pad encryption between two or more paired devices over any communication medium. A device generates key material from its hardware random number generator onto a memory card, which is handed to the other party in person. Before any key byte is used, the device records in F-RAM which part of the key has been consumed, so that no part can be used twice, even if the power fails at the moment of use. Its designs and software are public, and the project has received grant funding from the NGI0 Commons Fund.

## Quantum Computers

A **quantum computer** computes with quantum states rather than with ordinary bits. Large quantum computers do not yet exist, but if they are built, they will be able to break the public-key methods in common use today, including RSA, X25519 and Ed25519. Symmetric encryption and hash functions are much less affected: a 256-bit key remains secure.

Data that is recorded today and kept could be decrypted later, once such computers exist. For this reason new **post-quantum** public-key methods, based on mathematical problems that quantum computers are not known to solve, have been developed and standardized: ML-KEM for key exchange and ML-DSA for signatures, published as United States federal standards in 2024. Because these methods are newer and less studied, careful systems use them in a **hybrid** scheme together with a classical method, so that the result is secure as long as either one holds. The message protocol of Zeitlos, described in [The Machine](#the-machine), encrypts its connections in this way, although its signatures still use a classical method alone.

The one-time pad is unaffected by quantum computers, because its security does not depend on any calculation being difficult.

## Deleting Data

Deleting a file usually removes only its name and marks its space as free. The data remains on the medium until it is overwritten, and can often be recovered.

On flash memory, overwriting is not reliable either. Because of wear levelling, described in [Memory and Storage](#memory-and-storage), a new version of a block is written to a different place, and the old one may remain, inaccessible to the computer but readable by someone who reads the chip directly. The dependable method is to store sensitive data encrypted from the start, so that destroying the key destroys the data, wherever its copies lie. F-RAM, which is rewritten in place, can be overwritten directly. A medium that held secrets and is no longer needed can be physically destroyed.

## Secure Software

Every byte that arrives from a network, a file or a device may have been made to cause harm. A program that assumes its input has a certain length or form can be made to misbehave, as described under buffer overflows in [C](#c), and in the worst case to run instructions supplied by an attacker. Input is therefore checked before it is used, and programs that handle input from outside are kept small and simple.

Several practices limit the damage that a faulty or hostile program can do:

- **Least privilege.** Each program has only the access it needs. A program that cannot write to the system's files cannot damage them.
- **Few services.** Each program that accepts connections from a network is a possible way in. A machine that offers few services, and only to the network that needs them, has less to defend.
- **Protection boundaries.** Memory protection, described in [Operating Systems](#operating-systems), keeps one program from damaging another. Whether it is also a security boundary, which a hostile program cannot cross, depends on its design; a system may use it only to contain errors, as Zeitlos does.
- **Updates.** Weaknesses are found in all software, and fixes are published as updates. A small system has less code in which weaknesses can hide, and less to update.

Every program, library and tool on a machine is trusted to do what it claims, including the compiler that built the others. Ken Thompson showed in 1984 that a compiler could be altered to insert a weakness into the programs it compiles, including new copies of itself, so that the weakness appears in no source code. Software from a known source, checked against a published hash or signature, reduces what must be taken on trust; source code that can be read, and built again with independent tools to the same result, reduces it further.

## Copies

Offline copies of data, as described in [Computing That Lasts](#computing-that-lasts), are the defence against software that deletes or encrypts files and demands payment to restore them, as well as against every other kind of loss. A copy that is always connected can be reached by the same software, and is not a defence.

## Simplicity and Security

A simple system is easier to secure, because its owner can know what it runs, what it accepts from outside and what it stores. Each of the measures in this chapter is easier to apply to a small, well-understood machine than to a large one, and its effect is easier to check.

This completes the description of the machine: a processor, memory, devices, an operating system, a network and the means to protect them. The next part of the book is about programs.
