# Experiment Result

```json
{
  "experiment_id": "v014",
  "execution_provenance": "caller_recorded",
  "plan_sha256": "d8310e4d1b0265b10a77b235e71e88bc4f4edb435cde1141cd3e84a1d081266d",
  "candidate_sha256": "1b511d662b6cd951e2ffd2c95965b0fc4223636a30eb348ee68f973c80840e7f",
  "evidence_packet_sha256": "4d2735f63e9102db330636bfe635b0dd16739cab132f68ed1e61c46e2fb7b6be",
  "execution": {
    "command": "D:\\Desktop\\crl\\crl_agent_v3\\.venv\\python.exe -B D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\artifacts\\program_audit_r2.py --manifest D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\artifacts\\development_manifest.json --data-root D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\artifacts --official-detect D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\artifacts\\official_detect.py --config D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\artifacts\\config.json --rows-out D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\work\\dev_eval_001\\raw_rows.jsonl --summary-out D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\work\\dev_eval_001\\summary.json --cases-out D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\work\\dev_eval_001\\case_samples.json",
    "cwd": "D:\\Desktop\\crl\\20260722_1550_run01\\experiment_v014\\work\\dev_eval_001",
    "exit_code": 0,
    "stdout": "rows=10000\r\nunanimous_rows=9345\r\naccuracy_delta=0.016693418941\r\nbootstrap_95=[0.010464272172,0.023138725228]\r\ncorrections=157 regressions=1\r\npositive_models=9 positive_domains=5\r\nmechanism_transitions=157 mechanism_domains=5\r\nmechanical_gates=10/10\r\n",
    "stderr": "",
    "environment": {
      "capability": "12.0",
      "dataset_revision": "77ef18dadfc1ad96ce29c863f0913d990659432a",
      "gpu": "NVIDIA GeForce RTX 5060 Ti",
      "python": "3.11.15",
      "torch": "2.12.0+cu130",
      "torch_cuda": "13.0"
    }
  },
  "artifacts": [
    {
      "relative_path": "experiment_v014/artifacts/attempts_manifest.json",
      "byte_count": 4119,
      "sha256": "1b9689f17b93c72a46be8bb86e8ef1564bd731184a87c87e227c88e7ccaf3f9c"
    },
    {
      "relative_path": "experiment_v014/artifacts/candidate.md",
      "byte_count": 5199,
      "sha256": "1b511d662b6cd951e2ffd2c95965b0fc4223636a30eb348ee68f973c80840e7f"
    },
    {
      "relative_path": "experiment_v014/artifacts/config.json",
      "byte_count": 1398,
      "sha256": "aef60703933916e8c781af3e650ae735e0c664fdaca07d53face4052ae165e2f"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_acquisition_program.py",
      "byte_count": 2548,
      "sha256": "0b9dc76a10b75e2ad77c5745b2e10d6635da7f3bc0575e101a040ffd085c486a"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_acquisition_stderr.bin",
      "byte_count": 1035,
      "sha256": "a98541d77388f17dac3b81571524ae412c6dba0c5c531b84aa37e4e7c2c45ef5"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_acquisition_stdout.bin",
      "byte_count": 2070,
      "sha256": "71ada463328dab0a0dd11e4dbc5fa218817f6b38b44a2e0a8bdd35fb17721f43"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__claude-haiku-4-5_20260505_182847.json",
      "byte_count": 25936048,
      "sha256": "b479f1bdaaddd22eae68e9a7dc286d73d9523cf0e1e6dabddf0f130a1174d318"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__glm4-9b_20260505_165056.json",
      "byte_count": 25443195,
      "sha256": "ce694e4cc3d3eedec2f2e6401e172977d2d4ce4461120fd19fdf462a4f7b3a54"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__gpt-5.4-mini-2026-03-17_20260505_134938.json",
      "byte_count": 24612281,
      "sha256": "8d912c5a54c77b9dc09027395eee3fb0430e59b7f6c465553a7d34aade47492c"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__claude-haiku-4-5_judge_glm47_fp8_20260507_011748.json",
      "byte_count": 1160392,
      "sha256": "3daa1cbdd0e92fa65863913790ea7a0d3df9c2dfbc88228592b81ded52dc9c83"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__claude-haiku-4-5_judge_qwen35_397b_20260507_011208.json",
      "byte_count": 1281357,
      "sha256": "3f29556f14e459c80e6fc1e7e521406602e275709091735e7f37b2060a0eec62"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__glm4-9b_judge_glm47_fp8_20260507_013757.json",
      "byte_count": 1145095,
      "sha256": "eb80943f002f7d18d85d56eee60b51b49463831bd49755ee6e14ba2fc1183e41"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__glm4-9b_judge_qwen35_397b_20260507_012736.json",
      "byte_count": 1290754,
      "sha256": "7d77e21bd134e56ca04479fd20f23890218f3a8894a8a765b9aa3ea0ee27ae5a"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__gpt-5.4-mini-2026-03-17_judge_glm47_fp8_20260507_014451.json",
      "byte_count": 1132057,
      "sha256": "c0febfe5494b2ce53e469eb00d26988a610f0e933bfde04541d90dc2a80ca4cf"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__gpt-5.4-mini-2026-03-17_judge_qwen35_397b_20260507_013246.json",
      "byte_count": 1253161,
      "sha256": "bd45222fb9712330fd5dc1c09d7e2012be86dd23181393356ffa8e35803883ea"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__llama3.1-70b_judge_glm47_fp8_20260507_015415.json",
      "byte_count": 1159521,
      "sha256": "529395fcb4d0e44e97d2353a2f31d74188a62cbdec23f930d6d0da881260af81"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__llama3.1-70b_judge_qwen35_397b_20260507_014104.json",
      "byte_count": 1297741,
      "sha256": "cb66c4a2b28d68443ae6235d0645581f59eb9c9bda6f851aed3dc5b8f98c7c92"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__llama3.1-8b_judge_glm47_fp8_20260507_015623.json",
      "byte_count": 1148666,
      "sha256": "525f8c35f2cb49e41132f6c60fa8582eb1bf952533812fb323468ab8b8163483"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__llama3.1-8b_judge_qwen35_397b_20260507_014354.json",
      "byte_count": 1315303,
      "sha256": "d317e7b7fd7e17da4ed2caa819f0f3d7030ea78510a71fb04ce2fac69660444d"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__mistral-7b_judge_glm47_fp8_20260507_015919.json",
      "byte_count": 1136213,
      "sha256": "70093fe78fa120d72fddc3c7f72b03b2d2103950799122877458e6b797f96ef2"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__mistral-7b_judge_qwen35_397b_20260507_014627.json",
      "byte_count": 1310203,
      "sha256": "a897e5352741e65b2b9f194048da5bd3285a41ec8201dd34cb059912f5d3511b"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen2.5-32b-instruct_judge_glm47_fp8_20260507_020237.json",
      "byte_count": 1136557,
      "sha256": "f3230a6e4b87373727565b65037f1665b0ef0132940059ad883c8089b3ec09b9"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen2.5-32b-instruct_judge_qwen35_397b_20260507_014855.json",
      "byte_count": 1265880,
      "sha256": "13738d6deae3f2164d337d782807dd8140bce4bf057ca7c2ea4d7e6689130026"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen2.5-7b-instruct_judge_glm47_fp8_20260507_020942.json",
      "byte_count": 1150643,
      "sha256": "613cd7788bf97b184c6886de1624d99ab0e1a0689c9ccfb3246a895b08000cbf"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen2.5-7b-instruct_judge_qwen35_397b_20260507_015415.json",
      "byte_count": 1301965,
      "sha256": "1ad18eb4e25ca725cb0cac1a0f1faf2083d4bef3aa0da734976c50f5c5067c7e"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen3.5-9b_judge_glm47_fp8_20260507_021632.json",
      "byte_count": 1198095,
      "sha256": "797c80b8972c039c32c8ca0348e01b3c919d2b627159a2b935ef12b978a7d329"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen3.5-9b_judge_qwen35_397b_20260507_015956.json",
      "byte_count": 1301474,
      "sha256": "a2311d1c5309ce5fa64d1e368f349670ee9e0388f68630354e9a29f46d559783"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen3.6-27b_judge_glm47_fp8_20260507_021957.json",
      "byte_count": 1165068,
      "sha256": "e4f680f9a0643458bbb125e85a4ce1f2818bd4e0bed363024e7f2ef04a8cc72b"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen3.6-27b_judge_qwen35_397b_20260507_020236.json",
      "byte_count": 1260274,
      "sha256": "4a4668f391184ff50a271c5c1871584ace7d281827edeab22a0c5694ac228b6c"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen3.6-35b-a3b_judge_glm47_fp8_20260507_022330.json",
      "byte_count": 1184128,
      "sha256": "72dd5f9bba41b5fbdd98ae4de4a55336564a126de5796b7060efa41045501f67"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwen3.6-35b-a3b_judge_qwen35_397b_20260507_020535.json",
      "byte_count": 1285037,
      "sha256": "3f4ead4fa0a72a08d7e91a6e192b0da07f2299ba9f86b3a2d283d3495df717d7"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwq-32b_judge_glm47_fp8_20260507_022738.json",
      "byte_count": 1182262,
      "sha256": "f99b8c269e48f331abe8308d74dd6d7ec7651b2f4336cecddf10b2f3663ad91e"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__judge__qwq-32b_judge_qwen35_397b_20260507_020817.json",
      "byte_count": 1276165,
      "sha256": "c9de7d6bc95143b1636ba806cb07ee683939cc11f6c7aa6f7d384b474162f3c2"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__llama3.1-70b_20260506_024208.json",
      "byte_count": 24097885,
      "sha256": "ea444e55917f7415b97cf7eb680c452da10760f2d8cbfd92890a3abcd1a076eb"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__llama3.1-8b_20260505_121932.json",
      "byte_count": 24230500,
      "sha256": "574980c2bdd5dc811944377631e11f79a996543a419622d91d0c8ef7be37fedf"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__mistral-7b_20260506_002712.json",
      "byte_count": 24920399,
      "sha256": "332e53b9837ddafb60469818f5b5885b1a78d5ef0bd2a25a00837d2c6cf7be77"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__qwen2.5-32b-instruct_20260505_140237.json",
      "byte_count": 24551579,
      "sha256": "fd6bd8bbc6a1f0d9209e9a84f130720bfb4fabc1ff3605562521c0ef7579021d"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__qwen2.5-7b-instruct_20260505_122528.json",
      "byte_count": 24674072,
      "sha256": "a7900f59139500d05391cb08efde56919a2666e89f6edb218bf50113420323a7"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__qwen3.5-9b_20260505_134057.json",
      "byte_count": 27146853,
      "sha256": "d6237202e6e149d03265c8e42db90699101e55599de1772e3f921c24341073e2"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__qwen3.6-27b_20260506_045009.json",
      "byte_count": 29366114,
      "sha256": "6d570ddf32f363aa219ac0ffd53ca7f2f084c417630ac5a37446b1e01cdb8645"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__qwen3.6-35b-a3b_20260506_032809.json",
      "byte_count": 28924446,
      "sha256": "f1399cb17de69af5f2eee64bd7672291804fd2c8066b0954efe22bab2b0c05d7"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_input__qwq-32b_20260505_180119.json",
      "byte_count": 28834074,
      "sha256": "158df6bca02d19303c1cd05ebc717424af47c85ad9add276fff8aae5b99a4d25"
    },
    {
      "relative_path": "experiment_v014/artifacts/confirmation_manifest.json",
      "byte_count": 6921,
      "sha256": "f1076a79a00810308a8ebc496ba8ef25d22873560daac6f4aabeeb49a8011944"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_audit_001_execution.json",
      "byte_count": 2772,
      "sha256": "77f4164abdbd276a3d94244a4e6812b859f37de75f53ca281e4bd2511ebdba88"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_audit_001_report.json",
      "byte_count": 6712,
      "sha256": "99ca0a6733b128454b015e0dab7f94bab2f2b89dc3bb26b3878436b76759de4c"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_audit_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_audit_001_stdout.bin",
      "byte_count": 91,
      "sha256": "4e22b82575f53382b7acd8f1b03ee39a4a3c223cb2429738aed1f4a880226e9a"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_eval_001_case_samples.json",
      "byte_count": 75140,
      "sha256": "ebd851a176ad0c02408385afdbba0382586b539064f0374fc4d9c27cb687f8ec"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_eval_001_execution.json",
      "byte_count": 14485,
      "sha256": "6919473fcd8a8bb1210b8f125a4c581d7bb896e4dc926a3815db713417ec81d1"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_eval_001_raw_rows.jsonl",
      "byte_count": 10649156,
      "sha256": "5c50f38438621c18edbe1b34eb6595798b9d6980b7e96a18c3805a009f5dc8e8"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_eval_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_eval_001_stdout.bin",
      "byte_count": 250,
      "sha256": "7d4d1f60f7ce95713d1112359011476de8f8802712f97b94e6d392b74a56793d"
    },
    {
      "relative_path": "experiment_v014/artifacts/dev_eval_001_summary.json",
      "byte_count": 17019,
      "sha256": "4fd042ac7bf194452ac294c7e82534651b701fe60e778dac4fd7223eca60486a"
    },
    {
      "relative_path": "experiment_v014/artifacts/development_manifest.json",
      "byte_count": 7682,
      "sha256": "e5fc4a15ddc7f4b17e6cc04e9bc518fc53050ba11bc7b24ba026e703b161146e"
    },
    {
      "relative_path": "experiment_v014/artifacts/env_capture_001_execution.json",
      "byte_count": 1693,
      "sha256": "f301e325ef274aa5b40a3557bde57bfa4ed84856ebc8b978fa367f47c24a933c"
    },
    {
      "relative_path": "experiment_v014/artifacts/env_capture_001_stderr.bin",
      "byte_count": 0,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "relative_path": "experiment_v014/artifacts/env_capture_001_stdout.bin",
      "byte_count": 225,
      "sha256": "3331de8d0722cc4064a6e95d3dfd1eb29e61bb84713f0a553e01052c5599ba8e"
    },
    {
      "relative_path": "experiment_v014/artifacts/evidence_packet.md",
      "byte_count": 2561,
      "sha256": "4d2735f63e9102db330636bfe635b0dd16739cab132f68ed1e61c46e2fb7b6be"
    },
    {
      "relative_path": "experiment_v014/artifacts/implementation_audit.md",
      "byte_count": 6112,
      "sha256": "9781161295a8f01cebfa4e3e6bf262b8a06d90717d78df8253628e3be825a688"
    },
    {
      "relative_path": "experiment_v014/artifacts/implementation_audit_r2.md",
      "byte_count": 7141,
      "sha256": "85bc23c70a39c8ab3efe564bffa1ffa6e8231045d318761a6e8f2c72dd0da1eb"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__claude-sonnet-4_20260505_155750.json",
      "byte_count": 25786895,
      "sha256": "22d28b26decad608bb88b57da40ae65b7254c656a85e2f3f121cb7a535c6b05b"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__deepseek-r1-distill-llama-8b_20260505_155019.json",
      "byte_count": 34307947,
      "sha256": "53476d5aa578e1e6d3f13926273709c75e3e97024f4b001b22ee46840ce8ccb3"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__deepseek-v4-flash_20260505_154454.json",
      "byte_count": 25938811,
      "sha256": "9c0642990ca576ad456858faeb54c152fca40aea43426475ed5c91c51a7f040d"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__gemma4-27b-a4b_20260506_003436.json",
      "byte_count": 25278170,
      "sha256": "dc5d9f75554daceca934f32fba0314b16bc45a493cc6673c8233089a5019c37a"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__gemma4-31b_20260505_172309.json",
      "byte_count": 24556897,
      "sha256": "891ccd0e0ebcde487286c1f353874d5d967d71885fdae87639de77c34d71a826"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__glm4.7-flash_20260506_082356.json",
      "byte_count": 25228151,
      "sha256": "af9ba64cec0b0645e5a18b0bd3214ee9ebf29b4e141eaabcf8b3b467cd8a8ef4"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__grok-4-1-fast-reasoning_20260505_122910.json",
      "byte_count": 24885603,
      "sha256": "3f13d8853e7a767e2f6661e6852d800856cf923cb91429464641fef66a6e45e2"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__grok-4.3_20260505_135135.json",
      "byte_count": 24957894,
      "sha256": "ae7b1f28c843e449a64d11d37302dd8aed8690b61ab102747e4b6ed9bbe87f60"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__claude-sonnet-4_judge_glm47_fp8_20260507_012106.json",
      "byte_count": 1147028,
      "sha256": "572c1ee9a370a2125b6ccea5ffbd746612ee3be62258826be7168c8e34afec71"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__claude-sonnet-4_judge_qwen35_397b_20260507_011440.json",
      "byte_count": 1268042,
      "sha256": "b5bc155fbbf3c76030fc3933030f53c58fa5f617ee8c2d6399e4a9d057d43622"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__deepseek-r1-distill-llama-8b_judge_glm47_fp8_20260507_012450.json",
      "byte_count": 1227014,
      "sha256": "67417d56cf6f6490ddcbce6b5e247ab1b568adcd250623bc3fa1f699535be1de"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__deepseek-r1-distill-llama-8b_judge_qwen35_397b_20260507_011748.json",
      "byte_count": 1326513,
      "sha256": "3755d414d2ece59eca4665fb6abec9271df6507256b3bde196ad9746a3115a49"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__deepseek-v4-flash_judge_glm47_fp8_20260507_012813.json",
      "byte_count": 1166221,
      "sha256": "b86b81f750d67c1d02ae447cdfe71c3ca264e73fc2144a496cccc888b40c9be6"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__deepseek-v4-flash_judge_qwen35_397b_20260507_012024.json",
      "byte_count": 1282320,
      "sha256": "425afe7b65e8f8c2fb26c521b9c2de9e888cfd54a8cf79497381539436ecc8bf"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__gemma4-27b-a4b_judge_glm47_fp8_20260507_013127.json",
      "byte_count": 1133827,
      "sha256": "441580eedec63d27e008df7d641bbc2e648d435453f95f50c5ff1ce9235405c1"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__gemma4-27b-a4b_judge_qwen35_397b_20260507_012248.json",
      "byte_count": 1246151,
      "sha256": "8ab5401eb6d7b0290faba01be1111933160feedd5c75d91bacba74f05390c959"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__gemma4-31b_judge_glm47_fp8_20260507_013447.json",
      "byte_count": 1114680,
      "sha256": "f697f2a0c3e828bfe65a54127684aec783ff57795a38ad5411f7a4480e1a767a"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__gemma4-31b_judge_qwen35_397b_20260507_012509.json",
      "byte_count": 1227972,
      "sha256": "ba71968d5f31548c649bebb92217bfefc05c08bf603554a117088ad9c3dc675c"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__glm4.7-flash_judge_glm47_fp8_20260507_014126.json",
      "byte_count": 1125885,
      "sha256": "d3cbf586ca7966a09d5669e55f11f6c5c1726d71bfcc9c5d6eb2e07077018ad7"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__glm4.7-flash_judge_qwen35_397b_20260507_013019.json",
      "byte_count": 1253234,
      "sha256": "41ab80332753ad797ee402a19fbb09065e051571fa3dc068366cbe7cdf924ae8"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__grok-4-1-fast-reasoning_judge_glm47_fp8_20260507_014812.json",
      "byte_count": 1129487,
      "sha256": "0b916ea551dd20be348c5653da866dd86b5bcf44a2d57317d709f87c87ba821c"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__grok-4-1-fast-reasoning_judge_qwen35_397b_20260507_013514.json",
      "byte_count": 1249875,
      "sha256": "36921e119d58a8a9a34679b1aed2c39525bbb4ffa891218eac8af12042056a0d"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__grok-4.3_judge_glm47_fp8_20260507_015132.json",
      "byte_count": 1130531,
      "sha256": "90830eff264042efc034773f5fd3331473e781649ea5a15edbbd3f48b8876f15"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__grok-4.3_judge_qwen35_397b_20260507_013752.json",
      "byte_count": 1247394,
      "sha256": "4477ce3bb4c275496f3796702cbddbd490cab704e78bf2437744acb52ec5029b"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__qwen2.5-72b-instruct_judge_glm47_fp8_20260507_020604.json",
      "byte_count": 1141683,
      "sha256": "236b5e78f179c6cedd522732b07f049054893bf55cb4c7d2de5212dbc8d942bb"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__qwen2.5-72b-instruct_judge_qwen35_397b_20260507_015119.json",
      "byte_count": 1267712,
      "sha256": "3171ad84f6731cdc890c45e0610492b6c5d06428bdcae1b55fd9b044319225c2"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__qwen3.5-27b_judge_glm47_fp8_20260507_021300.json",
      "byte_count": 1185494,
      "sha256": "45e86613128b3061857cb45da48a6011318b3cc6213b2b1267e233847c09baf6"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge__qwen3.5-27b_judge_qwen35_397b_20260507_015711.json",
      "byte_count": 1279134,
      "sha256": "df540f9614b0e72e35b9be53d835a506450cc8f61f9c958404b54bdb6c38c86d"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__claude-sonnet-4_ensemble.json",
      "byte_count": 173799,
      "sha256": "d45bddf16230ed5e77fdfd42defd94ba900169453ad979ddf2225e0e0a9317fe"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__deepseek-r1-distill-llama-8b_ensemble.json",
      "byte_count": 177836,
      "sha256": "5ed66557ea85c49bcfb15a84ad7591ab435499f742ad7153b7b37672a3343afe"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__deepseek-v4-flash_ensemble.json",
      "byte_count": 174307,
      "sha256": "90b4320bd1ea04095fde0775407b249242cdffc2ffd7ac7a7cce191dc856c43d"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__gemma4-27b-a4b_ensemble.json",
      "byte_count": 173632,
      "sha256": "9486632f79adbb6ee9b10b8b9c15580f183a0a89d3fe890102ba8a364773b9c6"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__gemma4-31b_ensemble.json",
      "byte_count": 173118,
      "sha256": "20e3f4fd80cfd57d25fd33276aa6da646e992ba2d546dcd215fb59e3b9a04bfd"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__glm4.7-flash_ensemble.json",
      "byte_count": 173612,
      "sha256": "f76cdf30bfb79320a201a09a0d9fd0e00e22068dceaca43988690645a7a05d53"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__grok-4-1-fast-reasoning_ensemble.json",
      "byte_count": 173297,
      "sha256": "7f7fd4c69f31b8d259fd0a5c0160d931693221ddd809e941442b1c2c4841068c"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__grok-4.3_ensemble.json",
      "byte_count": 172593,
      "sha256": "293e77672d14d5a02fac7bc0da00b32e6cf64278b4feec685e03082ebad1eca6"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__qwen2.5-72b-instruct_ensemble.json",
      "byte_count": 172781,
      "sha256": "0e5928d22b6f45de4cf8a7181fec9ff6e279858dc9aa3e83fcffe995722e6a56"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__judge_ensemble__qwen3.5-27b_ensemble.json",
      "byte_count": 173133,
      "sha256": "7fe3d200d1dc4b514a95a95c7b766db80671397264d086375d50cc37271a08a6"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__qwen2.5-72b-instruct_20260506_110214.json",
      "byte_count": 25122545,
      "sha256": "ff7eb8eb6df020b4262079933f040571c58a4ea8b7ad9f54d9bc3941be1869b6"
    },
    {
      "relative_path": "experiment_v014/artifacts/input__qwen3.5-27b_20260505_161552.json",
      "byte_count": 26771981,
      "sha256": "fb90cf9e3589547daa64137f4d8201686c9722a26ecf076e25f8987d28db8125"
    },
    {
      "relative_path": "experiment_v014/artifacts/nearest_answer_equivalence.pdf",
      "byte_count": 545050,
      "sha256": "bd320a5183a6fb507f4e3ebfbff27eb76af647e68f55980ea4c6762907f62b40"
    },
    {
      "relative_path": "experiment_v014/artifacts/nearest_bfcl_changelog.md",
      "byte_count": 44359,
      "sha256": "27cbabdb95424b5b03b6b9b34eebdf99a5c5b64fc5d2964726ef42ecbac104db"
    },
    {
      "relative_path": "experiment_v014/artifacts/nearest_open_domain_qa.pdf",
      "byte_count": 1409447,
      "sha256": "61676b02aa277893a9ad9a4c9cf691a29ace32a47e6fe3b024d598632d318bd2"
    },
    {
      "relative_path": "experiment_v014/artifacts/nearest_prior.md",
      "byte_count": 4858,
      "sha256": "2a47ddbdc5b827e50ed6d046328d4773b7909356239937cd2ee8dc12851fe3a9"
    },
    {
      "relative_path": "experiment_v014/artifacts/official_detect.py",
      "byte_count": 6913,
      "sha256": "aee4d77596bdacb9025d85cccde766ff2a2ddbe1a291b6c143ea46d22863dbd0"
    },
    {
      "relative_path": "experiment_v014/artifacts/official_judge_base_rubric.md",
      "byte_count": 7108,
      "sha256": "a07f89a088a1f822fcab36c2370b9917598fe0353b2b4b92c327f513a7fa50e9"
    },
    {
      "relative_path": "experiment_v014/artifacts/official_judge_variant_a.md",
      "byte_count": 1909,
      "sha256": "f481ac6f12aa25f675df582941f955167293cf3e0f4e07e4d364dda75f872325"
    },
    {
      "relative_path": "experiment_v014/artifacts/official_judge_variant_b.md",
      "byte_count": 2401,
      "sha256": "15b3bd429c3a2e317a6dcc8b8e322b7ab8b0c0fc3c5e1631c9ffe69ce2319f63"
    },
    {
      "relative_path": "experiment_v014/artifacts/partition.json",
      "byte_count": 1380,
      "sha256": "c0bc90d4f429f79e394d7467d768b64f8471e82704b3f98a1666cf0092b6ec90"
    },
    {
      "relative_path": "experiment_v014/artifacts/partition_after_confirmation_acquisition.json",
      "byte_count": 1379,
      "sha256": "75fe902b57aa3e9a363c4efcbca7bbf0164678412089f023b385aa365acdddfe"
    },
    {
      "relative_path": "experiment_v014/artifacts/problem.md",
      "byte_count": 4563,
      "sha256": "72e2807e63f8c846118b6064624fa4a4981eb131e99d66f2f634b62985fa8723"
    },
    {
      "relative_path": "experiment_v014/artifacts/program_audit.py",
      "byte_count": 23443,
      "sha256": "b4f3f8fcb18c1fde12de5dfae04f739cae3605bf377671ec882710b8c0f39376"
    },
    {
      "relative_path": "experiment_v014/artifacts/program_audit_r2.py",
      "byte_count": 23500,
      "sha256": "6bc2a6d80a4cfdcf82ad6480e3d762dfb252b32f9be7d849c84466d12e47f057"
    },
    {
      "relative_path": "experiment_v014/artifacts/program_independent_audit.py",
      "byte_count": 12159,
      "sha256": "e6a7e4649aba4b62d9e2cb5cf8722f59b42058c8fdc7d83b5765471b5820ed3e"
    },
    {
      "relative_path": "experiment_v014/artifacts/promotion_audit.md",
      "byte_count": 7294,
      "sha256": "6cdf49c6da800891bf54a03e5306bb4745ea19c281ae694983fa45de15fc201f"
    },
    {
      "relative_path": "experiment_v014/artifacts/research_map.md",
      "byte_count": 8748,
      "sha256": "36911a08a1799535994373024e2417e0ef0b0e038c781b1c613aa02a321bfe1c"
    },
    {
      "relative_path": "experiment_v014/artifacts/selection_context.md",
      "byte_count": 10170,
      "sha256": "7b36ca33cfb2b11559f75a33c81beab5c0865ecf122f4c027d3822789b0cb061"
    },
    {
      "relative_path": "experiment_v014/artifacts/target_paper.pdf",
      "byte_count": 2549988,
      "sha256": "6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009"
    },
    {
      "relative_path": "experiment_v014/artifacts/test_audit.py",
      "byte_count": 2358,
      "sha256": "485c25ce67b5701f6e5a2c3131eddcf20098c1b335e1e54e5e7c92e698c3a553"
    },
    {
      "relative_path": "experiment_v014/artifacts/test_audit_r2.py",
      "byte_count": 2619,
      "sha256": "0cb9a63acb018faefc661234ad4470d646876742a69074cb8bc76da530dbf206"
    }
  ]
}
```

## Codex Interpretation

# v014 Result — Development positive; Confirmation execution contract blocked before science

## Disposition

`DEVELOPMENT_PROMOTED_CONFIRMATION_NOT_EXECUTED`

v014 produced strong positive Development evidence for Required-Grounding Precedence and a successful independent audit. The main Codex authorized Confirmation acquisition. The 12 trace and 24 judge files were then acquired from the preregistered fixed revision, with zero path overlap, zero hash/size error, and no ensemble file.

Before running the scientific program on those bytes, the main Codex found that the frozen v014 input-integrity implementation is Development-specific: it requires 10 traces, 20 judges, 10 unused ensembles, and 40 files. The Confirmation contract requires 12 traces, 24 judges, no ensembles, and 36 files. Running v014 would therefore violate either the frozen program or the frozen Confirmation contract.

No v014 Confirmation scientific argv was run and no Confirmation prediction, metric, case sample, or summary was created. The bytes were not parsed by the RGP evaluator.

## Development evidence

- 10,000 joined rows; 9,345 two-judge-unanimous rows.
- Official accuracy: `0.9295880149812734`.
- RGP accuracy: `0.9462814339218834`.
- Paired delta: `+0.016693418940609953`.
- Model-cluster bootstrap 95%: `[+0.010464272171620851, +0.02313872522763792]`.
- Corrections/regressions: `157/1`.
- Positive generator models: `9/10`.
- Positive domains: `5/5`.
- All Development gates: `10/10`.
- Independent audit exit `0`, `audit_ok=true`, metric error `0`.

The single Development regression is real: required values were present but the answer added unsupported HSR fee brackets. This bounds the claim to aggregate false-fabrication reduction and forbids claiming that required grounding rules out every extra fabrication.

## Execution-only continuation

The same Run must advance to v015. v015 may change only:

- manifest path mapping prefix needed for v015 frozen Artifacts;
- expected trace/judge/ensemble/file cardinalities from a config;
- phase-specific preregistered gates and input manifest identity;
- neutral output field naming from Development-specific to phase-generic terms.

v015 must not change RGP branch order, official predicates, judge selection, unanimity filter, metrics, bootstrap seed/resamples, Confirmation model/domain partition, or any scientific threshold. It must inherit v014 Development outputs without rerunning them. The already acquired Confirmation bytes may be copied and rehashed into v015 Artifacts, but their content must not be inspected before the corrected v015 Plan is published.

## State

- System: `DEVELOPMENT_NOT_COMMISSIONED`.
- Run: `ACTIVE`.
- Confirmation scientific result: absent.
- Review Packet: absent.
- Reviewers: not started.
- Decision: absent.
- Delivery: absent.
