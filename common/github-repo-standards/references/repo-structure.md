# Repo structure by language

The universal top-level shape is in `SKILL.md` Step 2. This file covers what goes *inside* the language-specific directory, since that's where conventions genuinely diverge.

## Python

Prefer the **src layout** over a flat layout for anything beyond a single-file script:

```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       └── ...
├── tests/
│   └── test_*.py
├── pyproject.toml
└── ...
```

**Why src layout over flat (`project_name/` at the repo root alongside `tests/`):** the flat layout lets tests accidentally import the package from the working directory rather than the installed package, masking packaging bugs that only surface after a real `pip install`. src layout forces tests to run against the installed package, which is what users will actually have.

Use `pyproject.toml` as the single source of packaging config (not a separate `setup.py` + `setup.cfg`, which is legacy). Tests live in `tests/`, mirroring the package's module structure. A `py.typed` marker file inside the package directory signals type-checker support if the project ships type hints.

## Node / TypeScript

```
project-name/
├── src/
├── dist/          (build output — gitignored, never committed)
├── tests/         (or co-located *.test.ts next to source files — pick one convention)
├── package.json
├── tsconfig.json  (if TypeScript)
└── ...
```

Never commit `dist/` or `node_modules/` — both are build output / installable dependencies, not source. `package.json`'s `main`/`module`/`types`/`exports` fields point at `dist/`, built by CI or a `prepublish` hook, not checked in. Co-located tests (`src/foo.ts` + `src/foo.test.ts`) scale better than a mirrored `tests/` tree once a project has many small modules; a separate `tests/` directory reads more clearly for a smaller, flatter project. Either is fine — consistency within the project matters more than which one.

## Go

```
project-name/
├── cmd/
│   └── project-name/
│       └── main.go
├── internal/      (private packages — importable only within this module)
├── pkg/           (public library packages — importable by other modules)
├── go.mod
└── go.sum
```

`cmd/<binary-name>/main.go` per binary the module produces (most modules produce exactly one, but this scales to several). `internal/` is enforced by the Go compiler itself — nothing outside this module tree can import it, which is the idiomatic way to mark implementation details as genuinely private rather than just "private by convention." Only use `pkg/` for code that's actually meant to be imported by other projects; if nothing outside this repo will ever import it, it belongs in `internal/` instead.

## Rust

```
project-name/
├── src/
│   ├── main.rs    (binary crate) or lib.rs (library crate)
│   └── ...
├── tests/         (integration tests — each file is a separate test binary)
├── benches/       (benchmarks, if using criterion or similar)
├── examples/      (runnable example programs)
└── Cargo.toml
```

Unit tests live inline in `src/` (`#[cfg(test)] mod tests`), colocated with the code they test — this is idiomatic Rust and different from most other languages' convention of a fully separate test tree. `tests/` is specifically for integration tests that exercise the crate's public API as an external consumer would.

## Java (Maven/Gradle)

```
project-name/
├── src/
│   ├── main/java/com/example/project/
│   └── test/java/com/example/project/
├── pom.xml        (Maven) or build.gradle (Gradle)
└── ...
```

This exact layout (`src/main/java`, `src/test/java`, mirrored package structure) is enforced by convention in both major build tools — deviating from it means fighting the build tool's defaults for no benefit.

## Generic / polyglot / no clear ecosystem

Use `src/` and `tests/` as the default, language-agnostic starting point, and adjust once the actual tooling (a specific framework, a specific build system) implies a different convention. Don't force a language-specific layout (like Go's `cmd/`/`internal/`/`pkg/` split) onto a project that isn't in that language — it signals conventions that don't apply and confuses contributors familiar with the actual ecosystem.

## Monorepos

A monorepo (multiple independently-versioned packages in one repo) doesn't get a single `src/`; instead:

```
repo-name/
├── packages/            (or apps/ + packages/ for app + shared-library split)
│   ├── package-a/
│   │   ├── src/
│   │   └── package.json (or equivalent per-language manifest)
│   └── package-b/
│       └── ...
├── README.md            (top-level: what this monorepo contains, how packages relate)
└── ...
```

Each package gets its own manifest and, for anything nontrivial, its own README covering package-specific usage — the root README should orient a newcomer across the whole repo, not duplicate every package's details. Community health files (CONTRIBUTING, CODE_OF_CONDUCT, etc.) live once at the repo root and apply to the whole monorepo, not per-package. CI typically needs path-based filtering so a change to one package doesn't trigger a full rebuild/test of every package — check whether the project already uses monorepo tooling (Nx, Turborepo, Lerna, Bazel) before hand-rolling this in a workflow file, since these tools solve exactly this problem.
