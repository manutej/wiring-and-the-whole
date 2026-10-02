.PHONY: verify witness e2 dogfood-grade dogfood-grade-toybank dogfood-grade-fineract-thin dogfood-grade-handler-wedge external-slice-check fetch-slice-dry-run fetch-slice-io-check fetch-slice-manifest-check pack-v0-check handler-family-pack-check cr-f95-stub-check pack-blind-eval-check pulse-gate pulse-eval pipeline-io wiringmap-check wiringmap-stress

verify:
	@./scripts/verify.sh

pulse-gate:
	@./scripts/pulse_gate.sh

pulse-eval:
	@bash scripts/pulse_eval_functional.sh

pipeline-io:
	@bash scripts/pipeline_world_io.sh

dogfood-grade:
	@python3 scripts/grade_l1_questions.py --answer-mode io

dogfood-grade-toybank:
	@python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-TOYBANK-QUESTIONS.json

dogfood-grade-fineract-thin:
	@python3 scripts/grade_l1_questions.py --answer-mode io --questions docs/dogfood/L1-FINERACT-THIN-QUESTIONS.json

dogfood-grade-handler-wedge:
	@python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-E3-COMMANDHANDLER-WEDGE-QUESTIONS.json

external-slice-check:
	@bash scripts/fineract_slice_check.sh

fetch-slice-dry-run:
	@bash scripts/fetch_fineract_slice.sh

fetch-slice-io-check:
	@bash scripts/fetch_slice_io_check.sh

fetch-slice-manifest-check:
	@python3 scripts/validate_slice_manifest.py

cr-f95-stub-check:
	@python3 scripts/cr_f95_stub_run.py --config experiments/cr-f95-stub/run_config.handler-wedge.v0.json

pack-blind-eval-check:
	@python3 scripts/pack_blind_eval_run.py --config experiments/pack-blind-eval/run_config.v0.json

wiringmap-stress:
	@bash scripts/wiringmap_stress.sh

wiringmap-check:
	@python3 -m pip install -q jsonschema
	@python3 scripts/validate_wiringmap.py
	@python3 scripts/extract_toybank_refs.py

pack-v0-check:
	@python3 scripts/build_l2_pack.py wiringmap/examples/toybank-accounts.v0.json
	@python3 scripts/reexpand_gate.py wiringmap/examples/toybank-accounts.v0.pack

handler-family-pack-check:
	@python3 scripts/build_handler_family_pack.py
	@python3 scripts/reexpand_gate.py fixtures/e3-commandhandler-wedge/pack
	@python3 -c "import json,pathlib; m=json.loads(pathlib.Path('fixtures/e3-commandhandler-wedge/manifest.json').read_text()); assert m['parsed']>=29, m"
	@python3 scripts/handler_family_token_report.py --write

witness:
	@python3 witness/run_witness.py

e2:
	@cd experiments && (test -f package-lock.json && npm ci --silent || npm install --silent)
	@cd experiments/e2-tokens && python3 e2_run.py
