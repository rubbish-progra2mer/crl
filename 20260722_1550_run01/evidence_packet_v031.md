# Evidence Packet v031

## Candidate identity

- Selection Context `cf6bbeccc45e31f90a5c07aa407bd6031cc3e5078538d67f7167725b2520c1dd`.
- Problem `7b67e73f005012af73e6fd9e1bd585755650855deb876ea752ab87783226d565`.
- Research Map `6d9bdb9d39b93649d3879f33f9b24e881ec2f816abe1cf733f70996691f52670`.
- Nearest Prior `78022d4ed5c53a7f9d03caf76dfbef81a2d25477f69aa6f3780f9a4afc5a8671`.
- Candidate `fdbbf978279d8a7fbfaea35ab9949054a8f671126ef2e641c9180b24f5948bd0`.

## Formal evidence

- P040 Card `paper-p040`, Card SHA-256 `354030f49ad220a8b00873e233fc9af64817ebedc3b887113ed1fa53e4198f2f`.
- P040 PDF SHA-256 `ab1307fdaaf97841bd09296bca225b736e8e9a712002ac123b1fab663f35ba6a`.

## Direct primary evidence

- Terminal Wrench `140df68e633bcb5544e37b67a6f362a917f7a38b566b25e1b42fe86beb619e8a`.
- Cheap Reward Hacking Detection `c5fd945125b1b6cd4739b2aacf150156bbfc8e47aff2d7240ea05ed697075ce0`.
- Trajectory Guard `ab6d2c66b081b32a90ff3f230854058199c049362ffb49f46bef9f869fc18d34`.

## Development data

The three exact dataset/manifest SHA pairs (six files) are frozen in the implementation config:

- bucket 1 dataset `d5daecba36e3e8f9c6bbe60c8e2b13e6206290d8ca7cddcf4a8cc27c2f82274f`; manifest `aa20ea73e71b7a3b9a41d444c8a8b7997216f0b85e53fbc5cffb663e25b67932`;
- bucket 2 dataset `bd766eb62cf98e8fb1b8dd17c20d5edfc759eeb737bd3c232f73e656f9e713a3`; manifest `9bcec296b8c380d21f084e60a860577a8e08b9188f8fce75d8c625a3671ee59e`;
- bucket 3 dataset `0e701e4c842e4f661ec8e8650ec157e5462efe93bbb5d2514aab6a6c8167d77a`; manifest `df2f4b46506978105121fe5afc36fcc2f1188dd1a5e6303cb2a2eef836cdc543`.

The reused base parser SHA-256 is `a29b8aace75bf5505620fab71c982e296e045cb1590a20a5a9c19a63c233d78d`.

## Frozen implementation

- program `2bd01db3af6b9e448df4cebbbd53d7e1bcf811f2bd588577954deaebecb18300`;
- independent auditor `b5e923337bf698f8d7a66a5519e757bf42aa245dd08c5effe7e8da1c7dddb3c5`;
- tests `13d3b8f9e28b633d0506d2e616652a05d66209f06225f004233d60a4d95cb347`;
- config `e98e37614cec3ce86bce8fd70f0634678e93b58f29c94734299d591d832dff55`;
- Implementation Audit `575d0d5645e42ce0a3c0cbade22b776f448a1db1eb9facdcb2616032e1baa665`;
- conditional acquisition `cf87ec4994081b4516695806b471daf75e923fe511d0b67d05b4ab126d34e836`;
- capture runner `410a620d0734613036f4fea4bc017c0cd1d0de293e1a3d4577c75eec584eaa4a`.

The cross-encoder directory contains exactly the six config-bound files:

- `config.json` `380e02c93f431831be65d99a4e7e5f67c133985bf2e77d9d4eba46847190bacc`;
- `model.safetensors` `821d1aa69520101d6e0737f78a042ae25b19e5cb9160701909d10434f4aeb0ae`;
- `special_tokens_map.json` `3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6`;
- `tokenizer.json` `d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66`;
- `tokenizer_config.json` `a5c2e5a7b1a29a0702cd28c08a399b5ecc110c263009d17f7e3b415f25905fd8`;
- `vocab.txt` `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3`.

## Isolation

No bucket-0 metadata, trajectory, label or task byte is present. No v031 score or control ranking existed when this Packet was finalized. The implementation, independent audit, tests, config and conditional acquisition path have been source-audited and hash-bound. This Packet authorizes only a publish-once Development Plan; it does not authorize Confirmation, Review or Delivery.
