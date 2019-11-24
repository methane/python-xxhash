import os
import unittest
import random
import xxhash


class TestXXH(unittest.TestCase):
    def test_xxh3_128(self):
        self.assertEqual(xxhash.xxh3_128('a').intdigest(), 14170847552498424646)
        self.assertEqual(xxhash.xxh3_128('a', 0).intdigest(), 14170847552498424646)
        self.assertEqual(xxhash.xxh3_128('a', 1).intdigest(), 12021697765055960290)
        self.assertEqual(xxhash.xxh3_128('a', 2**64-1).intdigest(), 1478388819684961177)

    def test_xxh3_128_intdigest(self):
        self.assertEqual(xxhash.xxh3_128_intdigest('a'), 14170847552498424646)
        self.assertEqual(xxhash.xxh3_128_intdigest('a', 0), 14170847552498424646)
        self.assertEqual(xxhash.xxh3_128_intdigest('a', 1), 12021697765055960290)
        self.assertEqual(xxhash.xxh3_128_intdigest('a', 2**64-1), 1478388819684961177)

    def test_xxh3_128_update(self):
        x = xxhash.xxh3_128()
        x.update('a')
        self.assertEqual(xxhash.xxh3_128('a').digest(), x.digest())
        self.assertEqual(xxhash.xxh3_128_digest('a'), x.digest())
        x.update('b')
        self.assertEqual(xxhash.xxh3_128('ab').digest(), x.digest())
        self.assertEqual(xxhash.xxh3_128_digest('ab'), x.digest())
        x.update('c')
        self.assertEqual(xxhash.xxh3_128('abc').digest(), x.digest())
        self.assertEqual(xxhash.xxh3_128_digest('abc'), x.digest())

        seed = random.randint(0, 2**64)
        x = xxhash.xxh3_128(seed=seed)
        x.update('a')
        self.assertEqual(xxhash.xxh3_128('a', seed).digest(), x.digest())
        self.assertEqual(xxhash.xxh3_128_digest('a', seed), x.digest())
        x.update('b')
        self.assertEqual(xxhash.xxh3_128('ab', seed).digest(), x.digest())
        self.assertEqual(xxhash.xxh3_128_digest('ab', seed), x.digest())
        x.update('c')
        self.assertEqual(xxhash.xxh3_128('abc', seed).digest(), x.digest())
        self.assertEqual(xxhash.xxh3_128_digest('abc', seed), x.digest())

    def test_xxh3_128_reset(self):
        x = xxhash.xxh3_128()
        h = x.intdigest()

        for i in range(10, 50):
            x.update(os.urandom(i))

        x.reset()

        self.assertEqual(h, x.intdigest())

    def test_xxh3_128_copy(self):
        a = xxhash.xxh3_128()
        a.update('xxhash')

        b = a.copy()
        self.assertEqual(a.digest(), b.digest())
        self.assertEqual(a.intdigest(), b.intdigest())
        self.assertEqual(a.hexdigest(), b.hexdigest())

        b.update('xxhash')
        self.assertNotEqual(a.digest(), b.digest())
        self.assertNotEqual(a.intdigest(), b.intdigest())
        self.assertNotEqual(a.hexdigest(), b.hexdigest())

        a.update('xxhash')
        self.assertEqual(a.digest(), b.digest())
        self.assertEqual(a.intdigest(), b.intdigest())
        self.assertEqual(a.hexdigest(), b.hexdigest())

    def test_xxh3_128_overflow(self):
        s = 'I want an unsigned 64-bit seed!'
        a = xxhash.xxh3_128(s, seed=0)
        b = xxhash.xxh3_128(s, seed=2**64)
        self.assertEqual(a.seed, b.seed)
        self.assertEqual(a.intdigest(), b.intdigest())
        self.assertEqual(a.hexdigest(), b.hexdigest())
        self.assertEqual(a.digest(), b.digest())
        self.assertEqual(a.intdigest(), xxhash.xxh3_128_intdigest(s, seed=0))
        self.assertEqual(a.intdigest(), xxhash.xxh3_128_intdigest(s, seed=2**64))
        self.assertEqual(a.digest(), xxhash.xxh3_128_digest(s, seed=0))
        self.assertEqual(a.digest(), xxhash.xxh3_128_digest(s, seed=2**64))
        self.assertEqual(a.hexdigest(), xxhash.xxh3_128_hexdigest(s, seed=0))
        self.assertEqual(a.hexdigest(), xxhash.xxh3_128_hexdigest(s, seed=2**64))

        a = xxhash.xxh3_128(s, seed=1)
        b = xxhash.xxh3_128(s, seed=2**64+1)
        self.assertEqual(a.seed, b.seed)
        self.assertEqual(a.intdigest(), b.intdigest())
        self.assertEqual(a.hexdigest(), b.hexdigest())
        self.assertEqual(a.digest(), b.digest())
        self.assertEqual(a.intdigest(), xxhash.xxh3_128_intdigest(s, seed=1))
        self.assertEqual(a.intdigest(), xxhash.xxh3_128_intdigest(s, seed=2**64+1))
        self.assertEqual(a.digest(), xxhash.xxh3_128_digest(s, seed=1))
        self.assertEqual(a.digest(), xxhash.xxh3_128_digest(s, seed=2**64+1))
        self.assertEqual(a.hexdigest(), xxhash.xxh3_128_hexdigest(s, seed=1))
        self.assertEqual(a.hexdigest(), xxhash.xxh3_128_hexdigest(s, seed=2**64+1))

        a = xxhash.xxh3_128(s, seed=2**65-1)
        b = xxhash.xxh3_128(s, seed=2**66-1)
        self.assertEqual(a.seed, b.seed)
        self.assertEqual(a.intdigest(), b.intdigest())
        self.assertEqual(a.hexdigest(), b.hexdigest())
        self.assertEqual(a.digest(), b.digest())
        self.assertEqual(a.intdigest(), xxhash.xxh3_128_intdigest(s, seed=2**65-1))
        self.assertEqual(a.intdigest(), xxhash.xxh3_128_intdigest(s, seed=2**66-1))
        self.assertEqual(a.digest(), xxhash.xxh3_128_digest(s, seed=2**65-1))
        self.assertEqual(a.digest(), xxhash.xxh3_128_digest(s, seed=2**66-1))
        self.assertEqual(a.hexdigest(), xxhash.xxh3_128_hexdigest(s, seed=2**65-1))
        self.assertEqual(a.hexdigest(), xxhash.xxh3_128_hexdigest(s, seed=2**66-1))


if __name__ == '__main__':
    unittest.main()
